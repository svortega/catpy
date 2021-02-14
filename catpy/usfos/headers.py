# 
# Copyright (c) 2009-2018 fem2ufo

#
# Python stdlib imports
import datetime
#

def print_head_line(head, subfix, length=84):
    """
    """
    text_out = []
    _head = str(head).upper()
    _space = length - 2 - len(_head)
    text_out.append("{:}\n".format(subfix))
    text_out.append("{:}\n".format(subfix))
    text_out.append("{:}{:}\n".format(subfix, length * '-'))
    text_out.append("{:}{:} {:}\n".format(subfix, _space * " ", _head))
    text_out.append("{:}{:}\n".format(subfix, length * '-'))
    text_out.append("{:}\n".format(subfix))
    text_out.append("{:}\n".format(subfix))
    return text_out
#
def print_title(Type, subfix, data=None):
    """
    """
    today = datetime.date.today()
    #
    text_out = []
    text_out.append("{:}{:}\n".format(subfix, 84 * '*'))
    
    text_out.append("{:}\n".format(subfix))
    text_out.append("{:}    {:} File Generated by fem2ufo Date : {:}\n"
                  .format(subfix, Type, str(today)))
    
    text_out.append("{:}\n".format(subfix))
    text_out.append("{:} {:} Version : {:} \n".format(subfix, 20 * ' ', '0.31 Beta (debug)'))
    text_out.append("{:} {:} Release Date : {:} \n".format(subfix, 15 * ' ', 'July, 2018'))
    text_out.append("{:} {:} download : http://bitbucket.org/svortega/fem2ufo/downloads\n"
                  .format(subfix, 19 * ' '))
    # text_out.append("{:} {:} document : http://fem2ufo.readthedocs.org\n".format(subfix, 40*' '))
    #text_out.append("{:} {:} Support : http://groups.google.com/group/fem2ufo_users\n"
    #              .format(subfix, 20 * ' '))
    text_out.append("{:} {:} Support : svortega@gmail.com\n".format(subfix, 20 * ' '))
    text_out.append("{:}\n".format(subfix))

    if data:
        text_out.append("{:}    Original FE Model:\n".format(subfix))
        text_out.append("{:}\n".format(subfix))
        for _key, _items in data.items():
            if _items.user != 'N/A':
                text_out.append("{:} -- {:} created by {:} ({:}) user: {:} the {:}\n"
                              .format(subfix, _items.file_name, _items.program, 
							          _items.version1, _items.user, _items.date))
        text_out.append("{:}\n".format(subfix))
    #
    text_out.append("{:}{:}\n".format(subfix, 84 * '*'))
    return text_out
#
# EOF
#
def print_EOF(subfix, length=84):
    """
    """
    text_out = []
    text_out.append("{:}\n".format(subfix))
    text_out.append("{:}{:}\n".format(subfix, length * '-'))
    text_out.append("{:}{:} fem2ufo is Python Powered \n".format(subfix, 32 * " "))
    text_out.append("{:}{:} http://www.python.org/ \n".format(subfix, 34 * " "))
    text_out.append("{:}{:} EOF \n".format(subfix, 43 * " "))
    text_out.append("{:}{:}\n".format(subfix, length * '-'))
    text_out.append("{:}\n".format(subfix))
    #
    return text_out
#
#
#
#
#