import org.apache.jena.OntModel;
import org.apache.jena.OntModelSpec;
import org.apache.jena.rdf.model.ModelFactory;

public class connectAndFind
{
      public static void main(String[] args)
      {
            if(args.length != 0)
            {
                  String namespace = "http://www.semanticweb.org/vindula/ontologies/2019/9/untitled-ontology-4#";
                  String file = "E:/Documents/test.owl";
                  
                  OntModel jenaModel = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);
                  //SparQL query goes here
                  if(args[0].equals("near"))
                  {
                        System.out.println(10.0);
                  }    

                  InputStream in = FileManager.get().open(file);
                  jenaModel.read(in, null);
            }
      }
}