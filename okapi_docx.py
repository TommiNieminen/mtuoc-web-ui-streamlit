import abc
import os.path
from lxml import etree
import sys
import re
import jpype
import jpype.imports
from jpype.types import *

class OkapiConnector():
    supported_file_extensions = [".docx"]

    def __init__(self):
        # Launch the JVM
        try:
            if not jpype.isJVMStarted():
                jpype.startJVM(classpath=['jars/mtuocokapiwrapper-1.0.jar'])
        except:
            pass
        from edu.uoc.mtuoc import MtuocOkapiWrapper
        self.okapi_wrapper = MtuocOkapiWrapper()

    def support(self, file_path: str):
        file_ext = os.path.splitext(file_path)[1]

        return file_ext in self.supported_file_extensions

    def get_output_path(self, file_path: str):
        dir_path = os.path.dirname(file_path)
        file_name, file_ext = os.path.splitext(os.path.basename(file_path))

        return dir_path + "/" + file_name + "_translated" + file_ext

    def sanitize_tags(self,line):
        enclosed_line = f"<line>{line}</line>\n"
        try:
            tree = etree.fromstring(enclosed_line)
            #sys.stderr.write(enclosed_line)
            return line
        except:
            sys.stderr.write(f"line tags are invalid, removing all tags: {line}\n")
            return re.sub("</{0,1}g[^>]*?>","",line) 

    def translate(self, translation_request, file_path: str, source_suffix: str, target_suffix: str, test_tags_only=False):

        self.okapi_wrapper.Extract(file_path,source_suffix,target_suffix)
        
        with open(f"{file_path}.{source_suffix}") as input_file, open(f"{file_path}.{target_suffix}",'wt') as output_file:
            for line in input_file:
                if line.strip():
                    #for tag testing, just translate lines with tags
                    if test_tags_only and "</g>" not in line:
                        output_file.write(f"NO TAGS: {line}")
                    else:
                        sanitized_translation = self.sanitize_tags(translation_request(line.rstrip()))
                        output_file.write(sanitized_translation + "\n")
                else:
                    #empty line handling
                    output_file.write("\n")

        self.okapi_wrapper.Merge(file_path,source_suffix,target_suffix)
        [prefix,ext] = os.path.splitext(file_path)
        return f"{prefix}.{target_suffix}{ext}"
