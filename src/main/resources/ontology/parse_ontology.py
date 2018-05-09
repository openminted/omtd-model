# import xml.etree.ElementTree as ET
from lxml import etree as ET
import sys,os,pprint,re,json,codecs,datetime,argparse

namespace = {
	"ms" : "http://www.meta-share.org/OMTD-SHARE_XMLSchema",
	"omtd-share" : "http://w3id.org/meta-share/omtd-share/",
	"oliatop" : "http://purl.org/olia/olia-top.owl#",
	"rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
	"owl" : "http://www.w3.org/2002/07/owl#",
	"xml" : "http://www.w3.org/XML/1998/namespace",
	"xsd" : "http://www.w3.org/2001/XMLSchema#",
	"skos" : "http://www.w3.org/2004/02/skos/core#",
	"rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
	"lappsgrid" : "http://vocab.lappsgrid.org/",
	"dc" : "http://purl.org/dc/elements/1.1/"
}

class Rename:

	@staticmethod
	def rename(name):
		if name is '':
			name = 'BLANK'
		elif name is 'null' :
			name = 'null'
		new_name = name
		match = re.match('^[^0-9][a-zA-Z_0-9]+$',name)
		if match is None:
			new_name = re.sub(r'\s',"",name)
			new_name = re.sub(r'/',"_",name)
			new_name = re.sub(r'[^\w\d_]','_', new_name)
			new_name = re.sub(r'([a-z])([A-Z])',r"\1_\2",new_name)
			if re.match('\d.*',new_name) is not None :
				new_name = 'V' + new_name
		else:
			new_name = re.sub(r'([a-z])([A-Z])',r"\1_\2",name)
		return new_name.upper()

class OwlClass :
	def __init__(self,node):
		self.id = node.attrib[ET.QName(namespace['rdf'], 'about')]
		comment = node.xpath(".//rdfs:comment",namespaces=namespace)
		self.comment = comment[0].text if len(comment) > 0 else None
		label = node.xpath(".//rdfs:label",namespaces=namespace)
		self.label = label[0].text if len(label) > 0 else None
		parents = node.xpath(".//rdfs:subClassOf[@rdf:resource]",namespaces=namespace)
		self.parents = []
		self.children = []
		for subClass in parents:
			self.parents.append(subClass.attrib[ET.QName(namespace['rdf'], 'resource')])

	def addChild(self,child):
		self.children.append(child)

def parseElements(filename) :
	tree = ET.parse(filename)
	root = tree.getroot()
	nodes = root.xpath(".//owl:Class",namespaces=namespace)
	ontologies = {}
	for owlClass in nodes :
		ontology = OwlClass(owlClass)
		ontologies[ontology.id] = ontology
	return ontologies

def buildTree(ontologies):
	topElements = []
	for key,ontology in ontologies.items():
		for parent in ontology.parents:
			if parent in ontologies:
				ontologies[parent].addChild(ontology)
			else:
				topElements.append(ontology)
	return topElements

def buildJson(ontology):
	properties = { 'id' : ontology.id, 'name' : ontology.label, 'comment' : ontology.comment }
	if len(ontology.children)!=0:
		properties['children'] = []
		for child in ontology.children:
			properties['children'].append(buildJson(child))
	return properties



if __name__ == '__main__' :
	parser = argparse.ArgumentParser(description="Parses the xsd files and injects code into the typescript generated file")
	parser.add_argument('-n', '--name', type=str, help = "the name of the generated typescript", default = "ontology.owl")
	parser.add_argument('-o', '--output', type=str, help = "the name of the generated typescript", default = "ontology.json")
	args = parser.parse_args()
	ontologies = parseElements(args.name)
	for ontology in ontologies:
		print Rename.rename(ontologies[ontology].id)+'='+ontologies[ontology].label
	topElements = buildTree(ontologies)
	jsonContent = []
	for ontology in topElements:
		jsonContent.append(buildJson(ontology))
	with codecs.open(args.output,'w',"utf-8") as f:
		f.write(json.dumps(jsonContent, indent=4))
		f.close()
