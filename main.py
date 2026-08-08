'''
Visualizes number of nucleotides in a given sequence
'''
from Bio import Entrez
import matplotlib.pyplot as plt

if __name__ == "__main__":

    #Accession for Drosophila melanogaster (clone 63B12) is AL021106.1
    #Accession for Caenorhabditis elegans (acr-16) is AY523511.1
    #Accession for Escherichia coli (16s rRNA) is NR_024570.1
    sequence = ""
    accession_number = input("Please enter the accession number from GenBank: ")

    try:
        with open("email.txt", "r") as email_file:
            Entrez.email = email_file.readline().strip()
            handle = Entrez.efetch(db="nucleotide", id=accession_number, rettype="gb", retmode="text")
            with open("sequence.gb", "w") as seq_file:
                for line in handle:
                    seq_file.write(line)
                handle.close()
    except FileNotFoundError:
        print("Could not find email")

    seq_type = ""
    definition = "Unknown Sequence"

    origin = False
    with open("sequence.gb", "r") as file:
        for line in file:
            if "Error:" in line:
                print("Invalid Accession Number")
                break
            if "DEFINITION" in line:
                definition = line.strip().split("  ")[1]
            if "/mol_type=" in line:
                if "DNA" in line:
                    seq_type = "DNA"
                elif "RNA" in line:
                    seq_type = "RNA"
                else:
                    print("Unknown Sequence Type")
                    break

            if "ORIGIN" in line:
                origin = True
                continue

            if origin:
                new_line = ""
                for segment in line:
                    for ch in segment:
                        ch = ch.lower()
                        if ch == "a" or ch == "t" or ch == "u" or ch == "c" or ch == "g":
                            new_line += ch
                sequence += new_line

    if not origin:
        print(f"No sequence information found for {definition}")

    if origin and not seq_type == "":
        bases = ["Adenine", "Thymine", "Uracil", "Cytosine", "Guanine"]
        counts = [0, 0, 0, 0]

        if seq_type == "DNA":
            bases.remove("Uracil")
        elif seq_type == "RNA":
            bases.remove("Thymine")

        for segment in sequence:
            for base in segment:
                if base.lower() == "a":
                    counts[0] += 1
                elif base.lower() == "t" or base.lower() == "u":
                    counts[1] += 1
                elif base.lower() == "c":
                    counts[2] += 1
                elif base.lower() == "g":
                    counts[3] += 1

        bar_colors = ["crimson", "lime", "gold", "turquoise"]
        plt.bar(bases, counts, label=bases, color=bar_colors)
        plt.ylabel("Abundance")
        plt.xlabel(f"Accession: {accession_number}")
        plt.title(f"Nucleotide Abundance in {definition}", wrap=True, fontsize=14)
        plt.show()
