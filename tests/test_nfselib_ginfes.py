# -*- coding: utf-8 -*-
# Copyright (C) 2019 - TODAY Raphaël Valyi - Akretion

import os
import sys
from os import path
from xmldiff import main
from lxml import etree as etree_
sys.path.append(path.join(path.dirname(__file__), '..', 'nfselib'))
from nfselib.ginfes.v3_01 import servico_enviar_lote_rps_envio as supermod


def parsexml_(infile, parser=None, keep_signature=False, **kwargs):
    "accepts both NFe and nfeProc documents"
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    if doc.getroot().tag == '{http://www.portalfiscal.inf.br/nfe}nfeProc':
        root = doc.getroot()[0]
    else:
        root = doc.getroot()
    # remove Signature element before XML comparison
    if not keep_signature:
        for child in root:
            if child.tag in ["{http://www.w3.org/2000/09/xmldsig#}Signature",
                             "{http://www.w3.org/2000/09/xmldsig#}\
                             ds:Signature"]:
                root.remove(child)
    subtree = etree_.ElementTree(root)
    return subtree

def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = supermod.get_root_tag(rootNode)
    if rootClass is None:
        rootClass = supermod.TNFe
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        export(rootObj)
    return rootObj


def export(doc, nfeProc=True, stream=sys.stdout):
    stream.write('<?xml version="1.0" ?>\n')
    if nfeProc:
        stream.write('<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" \
                         versao="4.00">\n')
    doc.export(stream, 0, namespaceprefix_='', name_='NFe',
               namespacedef_='xmlns="http://www.portalfiscal.inf.br/nfe"')
    if nfeProc:
        # TODO deal with infProt
        stream.write('</nfeProc>\n')


def test_in_out_leiauteNFe():
    path = 'nfse/ginfes'
    for filename in os.listdir(path):
        # primeiro filtramos a root tag e a possivel assinatura:
        subtree = parsexml_('%s/%s' % (path, filename,))
        inputfile = 'input.xml'
        subtree.write(inputfile, encoding='utf-8')

        # agora vamos importar o XML da nota e transforma-lo em objeto Python:
        obj = parse(inputfile)#'%s/%s' % (path, filename,))
        # agora podemos trabalhar em cima do objeto e fazer operaçoes como:
        obj.infNFe.emit.CNPJ

        outputfile = 'output.xml'
        with open(outputfile, 'w') as f:
            export(obj, nfeProc=False, stream=f)

        diff = main.diff_files(inputfile, outputfile)
        print(diff)
        assert len(diff) == 0
