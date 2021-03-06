# Copyright (C) 2012 Daniel Breakiron
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#

__author__ = 'breakid'

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
import os, sys
sys.path.append(os.path.abspath('./source'))
import conf

def setup(app):
    app.add_directive('inlineav',inlineav)


DIAGRAM = """\
<div id="%(exer_name)s">
</div>
"""

# div.jsavcanvas is required to ensure it appears before the error message otherwise the container appears over top of the message, blocking the 'Resubmit' link from being clicked
SLIDESHOW = """\
<div id="%(exer_name)s" class="ssAV" data-exer-name="%(exer_name)s" data-points="%(points)s" data-threshold="%(threshold)s" data-type="%(type)s" data-required="%(required)s" data-long-name="%(long_name)s">
 <span class="jsavcounter"></span>
 <a class="jsavsettings" href="#">Settings</a>
 <div class="jsavcontrols"></div>
 %(output_code)s
 <div class="jsavcanvas"></div>
 <img id="%(exer_name)s_check_mark" class="prof_check_mark" src="%(odsa_path)s/lib/Images/green_check.png" />
 <span id="%(exer_name)s_cm_saving_msg" class="cm_saving_msg">Saving...</span>
 <span id="%(exer_name)s_cm_error_msg" class="cm_error_msg">
  <img id="%(exer_name)s_cm_warning_icon" class="cm_warning_icon" src="_static/Images/warning.png" /><br />
  Server Error<br />
  <a href="#" class="resubmit_link">Resubmit</a>
 </span>
</div>
"""


def output(argument):
    """Conversion function for the "output" option."""
    return directives.choice(argument, ('show', 'hide'))

def type(argument):
    """Conversion function for the "output" option."""
    return directives.choice(argument, ('ss', 'diagram'))

class inlineav(Directive):
    required_arguments = 1
    optional_arguments = 6
    final_argument_whitespace = True
    option_spec = {
                   'output':output,
                   'required': directives.unchanged,
                   'long_name': directives.unchanged,
                   'points': directives.unchanged,
                   'threshold': directives.unchanged,
                   'type': type,
                  }

    def run(self):
        """ Restructured text extension for including inline JSAV content on module pages """
        self.options['exer_name'] = self.arguments[0]
        self.options['odsa_path'] = os.path.relpath(conf.odsa_path,conf.ebook_path)
        
        if 'required' not in self.options:
          self.options['required'] = False
        
        if 'points' not in self.options:
          self.options['points'] = 0
        
        if 'threshold' not in self.options:
          self.options['threshold'] = 1.0
          
        if 'type' not in self.options:
          self.options['type'] = 'diagram'
        
        if 'long_name' not in self.options:
          self.options['long_name'] = self.options['exer_name']
        
        if 'output' in self.options and self.options['output'] == "show":
          self.options['output_code'] = '<p class="jsavoutput jsavline" readonly="readonly"></p>'
        else:
          self.options['output_code'] = ''
        
        if self.options['type'] == "diagram":
          res = DIAGRAM % self.options
        else:
          res = SLIDESHOW % self.options
        return [nodes.raw('', res, format='html')]


source = """\
This is some text.

.. inlineav:: exer_name
   :output:

This is some more text.
"""

if __name__ == '__main__':
    from docutils.core import publish_parts

    directives.register_directive('inlineav',inlineav)

    doc_parts = publish_parts(source,
            settings_overrides={'output_encoding': 'utf8',
            'initial_header_level': 2},
            writer_name="html")

    print doc_parts['html_body']

