import tk.otfkb.demo.DemoSetup;

/**
 * @author datnb
 *
 */
public class OTFKB {
	private String host = "139.19.52.66";
	private String dataHost = "139.19.52.68";
	private DemoSetup demo;
	private static final int FACT_LIMIT = 6; // only consider 6 fields at most
	

	public OTFKB() {
		this.demo = new DemoSetup(host, dataHost);
	}

	/**
	 * TODO: may be better to return list of string
	 * 
	 * @param url
	 * @throws Exception
	 */
	public void buildKb(String url) throws Exception {
		for(String fact: demo.annotate(url, 1, -1, "web")) {
			if(fact.startsWith("[LOG]")) {
				// log info. Do nothing 
			}
			else if(fact.startsWith("[INFO]")) {
				// type info for filtering. Do nothing
			}
			else {
				if(fact.indexOf("; ;") == -1) { // noise: <Dylan; ; >
					if(fact.indexOf("[[", 2) == -1) {
						String[] tmp = fact.split("; ");
						if(tmp.length > 1 && tmp[1].split("_").length + 2 >= tmp.length
								&& tmp.length < FACT_LIMIT
								&& !tmp[1].equalsIgnoreCase("caption")) { // to remove noise: many components directly connect to verb
							// dump fact here
							System.out.println(fact);
						}
					}
				}
			}
		}
	}
	
	
	public static void main(String args[]) throws Exception {
		OTFKB tk = new OTFKB();
		String testUrl = "http://www.sparknotes.com/lit/potter2/summary.html";
		tk.buildKb(testUrl);
	}
	
	
}


