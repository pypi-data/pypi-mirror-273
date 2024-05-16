#!/usr/bin/env python3

"""
Pandoc filter to render metadata as jinja variables
"""

import panflute as pf

def prepare(doc):
    """ Load the doc metadata into a jinja Environment
    """
    doc.fenced_divs={}

def action(elem, doc):
    """ Analyze Div blocks
        if the Div is a recap, then replace the current elem by the recap list
        otherwise register the Div inside the global dictionnary
    """
    if isinstance(elem, pf.Div) and len(elem.classes) > 0:
        if elem.identifier == 'recap':
            return build_recap(elem,doc)

        # Else add the Div to the dictionary
        key = elem.classes[0]
        if not key in doc.fenced_divs.keys():
            doc.fenced_divs[key]=[]
        doc.fenced_divs[key].append(elem)
    return elem


def build_recap(elem, doc):
    """
    Create a new element, either a List or a new Div
    And inject the recap inside it
    """
    # the Div class to recap is not specified, exit immediatly
    if elem.classes == 0:
        return []

    key=elem.classes[0]

    # if there's nothing to recap, exit immediatly
    if key not in doc.fenced_divs or len(doc.fenced_divs[key]) == 0 :
        return []

    # For the first item, we have to initialize the container
    # In ordered or bullet lists, we inject a string representation of the
    # fenced div
    # Otherwise we inject the raw fenced div
    if 'OrderedList' in elem.classes:
        first_item=pf.Plain(pf.Str(pf.stringify(doc.fenced_divs[key][0])))
        recap=pf.OrderedList(pf.ListItem(first_item))
    elif 'BulletList' in elem.classes:
        first_item=pf.Plain(pf.Str(pf.stringify(doc.fenced_divs[key][0])))
        recap=pf.BulletList(pf.ListItem(first_item))
    else:
        recap=pf.Div(doc.fenced_divs[key][0],classes=["recap-"+key])

    # Add the other items
    index=1
    for item in doc.fenced_divs[key][1::]:
        if not isinstance(recap,pf.Div):
            recap.content.insert(index,pf.ListItem(pf.Plain(pf.Str(pf.stringify(item)))))
        else:
            recap.content.insert(index,item)
        index+=1

    return recap

def main(doc=None):
    """ Panflute setup
    """
    return pf.run_filter(action, prepare=prepare, doc=doc)

if __name__ == '__main__':
    main()
