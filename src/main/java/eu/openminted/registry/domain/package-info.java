@XmlSchema(namespace = "http://www.meta-share.org/OMTD-SHARE_XMLSchema",
        xmlns = {
                @XmlNs(namespaceURI = "http://www.meta-share.org/OMTD-SHARE_XMLSchema", prefix = "ms"),
                @XmlNs(namespaceURI = "http://www.w3.org/2001/XMLSchema-instance", prefix = "xsd")
        },
        elementFormDefault = javax.xml.bind.annotation.XmlNsForm.QUALIFIED)
package eu.openminted.registry.domain;

import javax.xml.bind.annotation.XmlNs;
import javax.xml.bind.annotation.XmlSchema;