import json

class DevSecAuditParser:

    def __init__(self, context):
        self.context = context
        self.inputfile = ''
        self.checkerfile = '' 
        self.owr_reportpath =  []
        self.property_name = 'ReportFile'

    def find_the_report_file(self, owr_reportpath, file_type, report_string):
        report_file = ''
        if len(owr_reportpath) != 0:
            for files in owr_reportpath:
                if files.endswith(file_type) and report_string in files:
                    return files
        return report_file

    def get_context_output(self, output_type, file_type, report_string, 
                           checker_file_type=None, checker_report_string=None):
        for output in self.context['Outputs']:
            if output["Type"] == output_type:
                self.owr_reportpath.extend(output[self.property_name])
        inputfile = self.find_the_report_file(self.owr_reportpath, file_type, report_string)
        checkerfile = self.find_the_report_file(self.owr_reportpath, checker_file_type, checker_report_string)
        return inputfile, checkerfile
    
    def get_report_files(self, output_type):
        scan_type = {"CoverityScan":{"type": "coverity", "file_type":"json", 
                                     "report_string":"coverity-report-result", 
                     "checkerfile":{"file_type":"json", 
                                    "report_string":"coverity-report-snapshot"}}}
        scan_selected = scan_type.get(output_type, None)
        if scan_selected:
            scan_selected_type = scan_selected["type"]
            file_type = scan_selected["file_type"]
            report_string = scan_selected["report_string"]
            checker_file_type = scan_selected["checkerfile"]["file_type"]
            checker_report_string = scan_selected["checkerfile"]["report_string"]
            self.inputfile, self.checkerfile = self.get_context_output(output_type, file_type, report_string, checker_file_type, checker_report_string)
            self.outputfile = self.inputfile.replace(f".{file_type}", "_sdle.xml")
            devsecaudit_cmd = f"devsecaudit run --type {scan_selected_type} --inputfile {self.inputfile},{self.checkerfile}  --outputfile {self.outputfile}"
            return devsecaudit_cmd

@click.command()
@click.option("--context", help="context data", required=True)
@click.option("--output_type",  help="scan type", required=True)
def get_scan_cmd(context: json, output_type: str):
    context = json.loads(context)
    devsecaudit_obj = DevSecAuditParser(context)
    devsecaudit_cmd = devsecaudit_obj.get_report_files(output_type)

    # to set output, print to shell in following syntax
    print(f"::set-output name=devsecaudit_cmd::{devsecaudit_cmd}")

if __name__ == '__main__':
    get_scan_cmd()
