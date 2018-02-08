import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.stream.Collectors;

public class ORFvoorspellerGUI extends JFrame {
    static JFileChooser chooser;
    static ActionListener actionall;
    static ActionListener actioninput;
    static ActionListener actionprocess;
    static JTextArea Viruslijstx;
    static JTextArea Viruslijsty;
    static JTextArea Overeenkomst;
    static JButton button;
    static JButton buttonentries;
    static JRadioButton r1;
    static JRadioButton r2;
    static JRadioButton r3;
    static String[] HostIDone;
    static String[] HostIDtwo;
    static String[] VirusClassification;
    static JScrollPane scrollone;
    static JScrollPane scrolltwo;
    static JScrollPane scrollthree;
    static ArrayList<ORFObject> ORFs;
    static ArrayList<String> ORFheaders;
    static ArrayList<String> ORFDNA;




    public static void main(String[] args) {
        ORFvoorspellerGUI f = new ORFvoorspellerGUI();
        f.setSize(800, 800);
        f.setTitle("Virus Applicatie");

        button = new JButton("Submit Bestand");
        button.setBounds(10,10,125,30);
        f.add(button);

        buttonentries = new JButton ("Predict ORFs");
        buttonentries.setBounds(375,300,150,40);
        f.add(buttonentries);

        JTextArea Summary = new JTextArea("De stappen zijn:\n\n1. Zoek Bestand in Chooser\n2. Druk op 'Open'\n3. Kies een Sortering\n4. Submit het bestand\n(5). (Optioneel):\nKijk naar de placeholders\n6. Submit de inputvelden\n7. Voor hergebruik,\n herstart programma");
        Summary.setBounds(10,50,170,280);
        f.add(Summary);

        r1=new JRadioButton("A) ID");
        r2=new JRadioButton("B) Classificatie");
        r3=new JRadioButton("C) Aantal Hosts");

        r1.setBounds(10,350,120,30);
        r2.setBounds(10,400,120,30);
        r3.setBounds(10,450,120,30);

        ButtonGroup bg=new ButtonGroup();
        bg.add(r1);bg.add(r2);bg.add(r3);

        f.add(r1);f.add(r2);f.add(r3);

        chooser = new JFileChooser();
        chooser.setBounds(200,10,500,300);
        f.add(chooser);

        VirusClassification = new String[] {"Placeholders : Please Select File or look at the placeholders","dsRNA", "ssRNA",
                "ssDNA", "Retrovirus","Satellite virus and Virophage","Viroid","Other"};
        //VirusClassList = new JComboBox<>(VirusClassification);

        //VirusClassList.setBounds(225,360,450,40);
        //f.add(VirusClassList);

        HostIDone = new String[] {"Placeholders","dsRNA Bacteria","dsRNA Eukaryota","dsRNA Archaea","dsRNA Viruses","dsRNA Unassigned/Other", "ssRNA Bacteria","ssRNA Eukaryota","ssRNA Archaea","ssRNA Viruses","ssRNA Unassigned/Other",
                "ssDNA Bacteria","ssDNA Eukaryota","ssDNA Archaea","ssDNA Viruses","ssDNA Unassigned/Other", "Retrovirus Bacteria","Retrovirus Eukaryota","Retrovirus Archaea","Retrovirus Viruses","Retrovirus Unassigned/Other","Satellite virus and Virophage Bacteria","Satellite virus and Virophage Eukaryota","Satellite virus and Virophage Archaea","Satellite virus and Virophage Viruses","Satellite virus and Virophage Unassigned/Other","Viroid Bacteria","Viroid Eukaryota","Viroid Archaea","Viroid Viruses","Viroid Unassigned/Other","Other Bacteria","Other Eukaryota","Other Archaea","Other Viruses","Other Unassigned/Other"};
        //HostIDoneList = new JComboBox<>(HostIDone);

        //HostIDoneList.setBounds(225,450,150,20);
        //f.add(HostIDoneList);

        HostIDtwo = new String[] {"Placeholders","dsRNA Bacteria","dsRNA Eukaryota","dsRNA Archaea","dsRNA Viruses","dsRNA Unassigned/Other", "ssRNA Bacteria","ssRNA Eukaryota","ssRNA Archaea","ssRNA Viruses","ssRNA Unassigned/Other",
                "ssDNA Bacteria","ssDNA Eukaryota","ssDNA Archaea","ssDNA Viruses","ssDNA Unassigned/Other", "Retrovirus Bacteria","Retrovirus Eukaryota","Retrovirus Archaea","Retrovirus Viruses","Retrovirus Unassigned/Other","Satellite virus and Virophage Bacteria","Satellite virus and Virophage Eukaryota","Satellite virus and Virophage Archaea","Satellite virus and Virophage Viruses","Satellite virus and Virophage Unassigned/Other","Viroid Bacteria","Viroid Eukaryota","Viroid Archaea","Viroid Viruses","Viroid Unassigned/Other","Other Bacteria","Other Eukaryota","Other Archaea","Other Viruses","Other Unassigned/Other"};
        //HostIDtwoList = new JComboBox<>(HostIDtwo);

        //HostIDtwoList.setBounds(525,450,150,20);
        //f.add(HostIDtwoList);

        String[] VirusLijstEen = new String[] {"HostID2"};
        //Virus1 = new JComboBox<>(VirusLijstEen);

        //Virus1.setBounds(525,450,150,20);
        //f.add(Virus1);

        Viruslijstx = new JTextArea("Placeholders", 6, 8);
        scrollone = new JScrollPane(Viruslijstx, JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scrollone.setBounds(225,550,150,60);
        f.add(scrollone);

        Viruslijsty = new JTextArea("Placeholders", 6, 8);
        scrolltwo = new JScrollPane(Viruslijsty, JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scrolltwo.setBounds(525,550,150,60);
        f.add(scrolltwo);

        Overeenkomst = new JTextArea("Placeholders", 6, 8);
        scrollthree = new JScrollPane(Overeenkomst, JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scrollthree.setBounds(375,650,150,60);
        f.add(scrollthree);

        JLabel L1=new JLabel("Virusclassificatie");
        L1.setBounds(225,330,450,40);
        JLabel L2=new JLabel("Viruslijst 1");
        L2.setBounds(225,530,150,20);
        JLabel L3=new JLabel("Viruslijst 2");
        L3.setBounds(525,530,150,20);
        JLabel L4=new JLabel("Virusovereenkomst");
        L4.setBounds(375,630,150,20);
        JLabel L5=new JLabel("Hostlijst 1");
        L5.setBounds(225,430,150,20);
        JLabel L6=new JLabel("Hostlijst 2");
        L6.setBounds(525,430,150,20);
        JLabel L7=new JLabel("Sortering");
        L7.setBounds(10,330,170,20);
        L7.setFont(new Font("Papyrus", Font.BOLD, 18));
        f.add(L1);f.add(L2);f.add(L3);f.add(L4);f.add(L5);f.add(L6);f.add(L7);

        f.setLayout(null);
        f.setVisible(true);

        main2(new String[] {"start"});
    }
    public ORFvoorspellerGUI() {
        actionall = new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    File selectedFile = chooser.getSelectedFile();

                    //Tijdelijk: Hier kan nu gekozen worden de ene uit te commenten of de andere
                    BufferedReader r = new BufferedReader(new FileReader("D:/\\Bio-Infmap/Data/Periode 7/H5N1seq1.fasta"));
                    //BufferedReader r = new BufferedReader(new FileReader(selectedFile));

                    ORFs = new ArrayList<>();
                    ORFDNA = new ArrayList<>();
                    ORFheaders = new ArrayList<>();

                    for (String x = r.readLine(); x != null; x = r.readLine()) {
                        String y = "";
                        String z = "";
                        StringBuilder s = new StringBuilder();

                        if (x.startsWith(">")) {
                            y = x;
                        }

                        if (!x.startsWith(">")) {
                            z = x;

                            s.append(z);

                        }
                        ORFObject ORFEntry = new ORFObject(y, z);
                        s.setLength(0);
                        ORFs.add(ORFEntry);
                    }

                    System.out.println(ORFs);
                    for (ORFObject orf : ORFs) {
                        ORFDNA.add(orf.getDNA());
                        System.out.println(orf.getDNA());
                    }
                    for (ORFObject orf : ORFs) {
                        ORFheaders.add(orf.getHeader());
                        System.out.println(orf.getHeader());
                    }

                    //buttonentries.doClick();

                } catch (IOException IO) {
                    System.out.println("IO Error, Bestand is Niet Goed Geladen");

                } catch (java.lang.NumberFormatException jln) {
                    System.out.println("Dit is geen goed Bestand");

                } catch (Exception x) {
                    System.out.println("Een Exception vond plaats");
                    System.out.println(x.toString());
                }
            }
        };
    }

    public static void main2(String[] argsFirst) {
        //button.addActionListener(VirusGUI.actionall);
        buttonentries.addActionListener(actionall);
        //buttonentries.addActionListener(actionprocess);
    }
}
