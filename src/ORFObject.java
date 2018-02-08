public class ORFObject {
    private String header;
    private String DNA;




    public ORFObject(String head, String DNAstring) {
        setHeader(head);
        setDNA(DNAstring);
    }


    public String getHeader() {
        return header;
    }

    public void setHeader(String header) {
        this.header = header;
    }

    public String getDNA() {
        return DNA;
    }

    public void setDNA(String DNA) {
        this.DNA = DNA;
    }
}
