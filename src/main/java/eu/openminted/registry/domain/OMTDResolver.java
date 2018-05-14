package eu.openminted.registry.domain;

public class OMTDResolver {

    static public IdentificationInfo resolveIdentificationInfo(BaseMetadataRecord resource) {
        if (resource instanceof Component) {
            return ((Component) resource).getComponentInfo().getIdentificationInfo();
        } else if (resource instanceof Corpus) {
            return ((Corpus) resource).getCorpusInfo().getIdentificationInfo();
        } else if (resource instanceof Lexical) {
            return ((Lexical) resource).getLexicalConceptualResourceInfo().getIdentificationInfo();
        } else if (resource instanceof LanguageDescription) {
            return ((LanguageDescription) resource).getLanguageDescriptionInfo().getIdentificationInfo();
        } else {
            return null;
        }
    }
}
