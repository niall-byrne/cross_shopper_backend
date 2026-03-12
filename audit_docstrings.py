"""Utility script to audit docstrings in the Cross Shopper project."""

import ast
import os
from collections import defaultdict


def audit_file(filepath):
  """Audit a single python file for docstring abnormalities."""
  with open(filepath, 'r') as f:
    try:
      content = f.read()
      tree = ast.parse(content)
    except SyntaxError:
      return [f"Syntax Error in {filepath}"]

  abnormalities = []
  docstrings_in_file = defaultdict(list)

  # 1. Module-level docstring
  module_doc = ast.get_docstring(tree)
  if module_doc:
    if "accross" in module_doc.lower():
      abnormalities.append("Found 'accross' in module docstring")

    if ('report_target' in filepath and 'ReportTarget' not in module_doc and
        'Reports' in module_doc):
      if 'report_pricing' not in filepath:
        abnormalities.append(
            "Module docstring might reference 'Reports' instead of "
            "'ReportTarget'"
        )

    if ('report_summary' in filepath and 'ReportSummary' not in module_doc and
        'Report ' in module_doc):
      abnormalities.append(
          "Module docstring might reference 'Report' instead of 'ReportSummary'"
      )

  for node in ast.walk(tree):
    # Only check nodes that can have docstrings
    if isinstance(
        node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
    ):
      docstring = ast.get_docstring(node)
      if docstring:
        if "accross" in docstring.lower():
          abnormalities.append(
              f"Found 'accross' in docstring: {repr(docstring[:50])}..."
          )

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
          docstrings_in_file[docstring].append(node.name)

    # 2. Class-level docstring context
    if isinstance(node, ast.ClassDef):
      class_docstring = ast.get_docstring(node)
      if class_docstring:
        # Check for wrong model in Serializer/Factory/Filter
        model_name = None
        for subnode in node.body:
          if isinstance(subnode, ast.ClassDef) and subnode.name == 'Meta':
            for item in subnode.body:
              if isinstance(item, ast.Assign):
                for target in item.targets:
                  if isinstance(target, ast.Name) and target.id == 'model':
                    if isinstance(item.value, ast.Name):
                      model_name = item.value.id
                    elif isinstance(item.value, ast.Constant):
                      model_name = item.value.value.split('.')[-1]

        if model_name and model_name.lower() not in class_docstring.lower():
          # Special cases
          if not (model_name == "User" and "user" in class_docstring.lower()
                 ) and not (model_name == "Price" and
                            "pricing" in class_docstring.lower()) and not (
                                model_name == "Item" and
                                "items" in class_docstring.lower()) and not (
                                    model_name == "Country" and
                                    "countries" in class_docstring.lower()
                                ) and not (model_name == "Locality" and
                                           "localities" in class_docstring.lower
                                           ()):
            abnormalities.append(
                f"Class '{node.name}' docstring might reference wrong model "
                f"(expected '{model_name}'). Found: {repr(class_docstring)}"
            )

        # Check for mismatch between Class Name and Docstring
        if node.name.startswith('Test'):
          if ('ReportTarget' in node.name and 'Reports' in class_docstring and
              'ReportTarget' not in class_docstring):
            abnormalities.append(
                f"Class '{node.name}' docstring references 'Reports' but class "
                "is for 'ReportTarget'"
            )
          if ('ReportSummary' in node.name and 'Report ' in class_docstring and
              'ReportSummary' not in class_docstring):
            abnormalities.append(
                f"Class '{node.name}' docstring references 'Report' but class "
                "is for 'ReportSummary'"
            )

          # Specific check for TestReportsReadOnlyViewSetCreate in report_target
          if ('report_target' in filepath and
              'ReportTarget' not in node.name and 'Reports' in node.name):
            abnormalities.append(
                f"Class '{node.name}' in {os.path.basename(filepath)} might be "
                "named incorrectly (references 'Reports' instead of "
                "'ReportTarget')"
            )

  # 3. Method-level docstring
  for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
      is_test = node.name.startswith('test_')
      is_fixture = False
      for dec in node.decorator_list:
        if (isinstance(dec, ast.Attribute) and dec.attr == 'fixture') or \
           (isinstance(dec, ast.Call) and
            isinstance(dec.func, ast.Attribute) and
            dec.func.attr == 'fixture') or \
           (isinstance(dec, ast.Name) and dec.id == 'fixture'):
          is_fixture = True

      method_docstring = ast.get_docstring(node)

      if is_test or is_fixture:
        if method_docstring:
          abnormalities.append(
              f"Docstring found in {'test' if is_test else 'fixture'} "
              f"'{node.name}' (should be avoided)"
          )
      else:
        # Special check for __repr__ and caching
        if node.name == '__repr__':
          expected_caching_doc = "Control caching behaviour across instances."
          if "serializer" in filepath.lower():
            if method_docstring != expected_caching_doc:
              abnormalities.append(
                  "__repr__ in serializer missing/incorrect caching docstring. "
                  f"Found: {repr(method_docstring)}"
              )

  # Check for duplicate docstrings for different methods in the same file
  for doc, methods in docstrings_in_file.items():
    if len(methods) > 1:
      if doc.strip():
        abnormalities.append(
            f"Duplicate docstring {repr(doc)} found in methods: "
            f"{', '.join(methods)}"
        )

  return abnormalities


def main():
  """Scan the project and print the audit report."""
  root_dir = 'cross_shopper'
  report = {}

  for root, _, files in os.walk(root_dir):
    for file in files:
      if file.endswith('.py'):
        filepath = os.path.join(root, file)
        file_abnormalities = audit_file(filepath)
        if file_abnormalities:
          report[filepath] = file_abnormalities

  # Additional manual findings from inspection
  manual_findings = {
      "cross_shopper/api/views/report_target/tests/"
      "test_report_target_list.py":
          [
              "Class 'TestReportTargetReadOnlyViewSetList' methods use generic "
              "Report objects but docstring is 'Test for the "
              "ReportTargetReadOnlyViewSet list view.' (correct but generic)"
          ],
      "cross_shopper/api/views/report_target/tests/"
      "test_report_target_create.py":
          [
              "Class 'TestReportsReadOnlyViewSetCreate' is named incorrectly "
              "for ReportTarget tests (should be TestReportTarget...)"
          ],
      "cross_shopper/api/views/report_summary/tests/"
      "test_report_summary_create.py":
          [
              "Class 'TestReportReadOnlyViewSet' is named incorrectly for "
              "ReportSummary tests (should be TestReportSummary...)",
              "Class 'TestReportReadOnlyViewSet' docstring is 'Test for the "
              "ReportReadOnlyViewSet create view.' (should be "
              "ReportSummary...)"
          ]
  }

  for fp, abns in manual_findings.items():
    if fp in report:
      report[fp].extend(abns)
    else:
      report[fp] = abns

  # Format as Markdown
  print("# Docstring Audit Report\n")
  if not report:
    print("No abnormalities found.")
  else:
    for filepath, abnormalities in sorted(report.items()):
      print(f"## `{filepath}`")
      for a in abnormalities:
        print(f"- {a}")
      print()


if __name__ == "__main__":
  main()
