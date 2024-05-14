import os 
from Bio import SeqIO
from Bio.Seq import MutableSeq
import numpy as np
import h5py
import time
import argparse
import spliceaitoolkit.create_data.utils as utils

donor_motif_counts = {}  # Initialize counts
acceptor_motif_counts = {}  # Initialize counts

def get_sequences_and_labels(db, fasta_file, output_dir, seq_dict, data_type, chrom_dict, parse_type="maximum", biotype="protein-coding"):
    """
    Extract sequences for each protein-coding gene, reverse complement sequences for genes on the reverse strand,
    and label donor and acceptor sites correctly based on strand orientation.
    """
    fw_stats = open(f"{output_dir}stats.txt", "w")
    NAME = []      # Gene Name
    CHROM = []     # Chromosome
    STRAND = []    # Strand in which the gene lies (+ or -)
    TX_START = []  # Position where transcription starts
    TX_END = []    # Position where transcription ends
    SEQ = []       # Nucleotide sequence
    LABEL = []     # Label for each nucleotide in the sequence
    h5fname = None
    if biotype =="non-coding":
        h5fname = output_dir + f'datafile_{data_type}_ncRNA.h5'
    elif biotype =="protein-coding":
        h5fname = output_dir + f'datafile_{data_type}.h5'
    h5f = h5py.File(h5fname, 'w')
    GENE_COUNTER = 0
    for gene in db.features_of_type('gene'):
        if "exception" in gene.attributes.keys() and gene.attributes["exception"][0] == "trans-splicing":
            continue
        if gene.seqid not in chrom_dict:
            continue
        if biotype =="protein-coding":
            if gene.attributes["gene_biotype"][0] != "protein_coding":
                continue
        elif biotype =="non-coding":
            if gene.attributes["gene_biotype"][0] != "lncRNA" and gene.attributes["gene_biotype"][0] != "ncRNA":
                continue
        else:
            continue
        chrom_dict[gene.seqid] += 1
        gene_id = gene.id
        ############################################
        # Process the gene sequence
        ############################################
        gene_seq = seq_dict[gene.seqid].seq[gene.start-1:gene.end].upper()  # Extract gene sequence
        if gene.strand == '-':
            gene_seq = gene_seq.reverse_complement() # reverse complement the sequence
        gene_seq = str(gene_seq.upper())
        print(f"Processing gene {gene_id} on chromosome {gene.seqid}..., len(gene_seq): {len(gene_seq)}")
        labels = [0] * len(gene_seq)  # Initialize all labels to 0
        if biotype =="protein-coding":
            transcripts = list(db.children(gene, featuretype='mRNA', order_by='start'))
        elif biotype =="non-coding":
            transcripts = list(db.children(gene, level=1, order_by='start'))
        if len(transcripts) == 0:
            continue
        elif len(transcripts) > 1:
            print(f"Gene {gene_id} has multiple transcripts: {len(transcripts)}")
        ############################################
        # Selecting which mode to process the data
        ############################################
        transcripts_ls = []
        if parse_type == 'maximum':
            max_trans = transcripts[0]
            max_len = max_trans.end - max_trans.start + 1
            for transcript in transcripts:
                if transcript.end - transcript.start + 1 > max_len:
                    max_trans = transcript
                    max_len = transcript.end - transcript.start + 1
            transcripts_ls = [max_trans]
        elif parse_type == 'all_isoforms':
            transcripts_ls = transcripts
        
        # Process transcripts
        for transcript in transcripts_ls:
            exons = list(db.children(transcript, featuretype='exon', order_by='start'))
            if len(exons) > 1:
                GENE_COUNTER += 1
                for i in range(len(exons) - 1):
                    # Donor site is one base after the end of the current exon
                    first_site = exons[i].end - gene.start  # Adjusted for python indexing
                    # Acceptor site is at the start of the next exon
                    second_site = exons[i + 1].start - gene.start  

                    # Adjusted for python indexing
                    if gene.strand == '+':
                        d_idx = first_site
                        a_idx = second_site
                    elif gene.strand == '-':
                        d_idx = len(labels) - second_site-1
                        a_idx = len(labels) - first_site-1
                        # print(f"Gene {gene_id} is on the reverse strand, d_idx: {d_idx}, a_idx: {a_idx}; len(labels): {len(labels)}")
                    ############################################
                    # Check if the donor / acceptor sites are valid
                    ############################################
                    d_motif = str(gene_seq[d_idx+1:d_idx+3])
                    a_motif = str(gene_seq[a_idx-2:a_idx])
                    if (d_motif == "GT" and a_motif == "AG") or (d_motif == "GC" and a_motif == "AG") or (d_motif == "AT" and a_motif == "AC"):
                        labels[d_idx] = 2   # Mark donor site
                        labels[a_idx] = 1  # Mark acceptor site
            labels_str = ''.join(str(num) for num in labels)
            NAME.append(gene_id)
            CHROM.append(gene.seqid)
            STRAND.append(gene.strand)
            TX_START.append(str(gene.start))
            TX_END.append(str(gene.end))
            SEQ.append(gene_seq)
            LABEL.append(labels_str)
            fw_stats.write(f"{gene.seqid}\t{gene.start}\t{gene.end}\t{gene.id}\t{1}\t{gene.strand}\n")
            utils.check_and_count_motifs(gene_seq, labels, gene.strand, donor_motif_counts, acceptor_motif_counts)
    fw_stats.close()
    dt = h5py.string_dtype(encoding='utf-8')
    h5f.create_dataset('NAME', data=np.asarray(NAME, dtype=dt) , dtype=dt)
    h5f.create_dataset('CHROM', data=np.asarray(CHROM, dtype=dt) , dtype=dt)
    h5f.create_dataset('STRAND', data=np.asarray(STRAND, dtype=dt) , dtype=dt)
    h5f.create_dataset('TX_START', data=np.asarray(TX_START, dtype=dt) , dtype=dt)
    h5f.create_dataset('TX_END', data=np.asarray(TX_END, dtype=dt) , dtype=dt)
    h5f.create_dataset('SEQ', data=np.asarray(SEQ, dtype=dt) , dtype=dt)
    h5f.create_dataset('LABEL', data=np.asarray(LABEL, dtype=dt) , dtype=dt)
    h5f.close()


def create_datafile(args):
    os.makedirs(args.output_dir, exist_ok=True)
    db = utils.create_or_load_db(args.annotation_gff, db_file=f'{args.annotation_gff}_db')
    seq_dict = SeqIO.to_dict(SeqIO.parse(args.genome_fasta, "fasta"))
    # TRAIN_CHROM_GROUP, TEST_CHROM_GROUP = utils.split_chromosomes(seq_dict, split_ratio=0.8, chr_split=args.chr_split)
    TRAIN_CHROM_GROUP = {
        'chr2': 0, 'chr4': 0, 'chr6': 0, 'chr8': 0, 
        'chr10': 0, 'chr11': 0, 'chr12': 0, 'chr13': 0,
        'chr14': 0, 'chr15': 0, 'chr16': 0, 'chr17': 0, 
        'chr18': 0, 'chr19': 0, 'chr20': 0, 'chr21': 0, 
        'chr22': 0, 'chrX': 0, 'chrY': 0
    }
    TEST_CHROM_GROUP = {
        'chr1': 0, 'chr3': 0, 'chr5': 0, 'chr7': 0, 'chr9': 0
    }
    print("TRAIN_CHROM_GROUP: ", TRAIN_CHROM_GROUP)
    print("TEST_CHROM_GROUP: ", TEST_CHROM_GROUP)
    print("--- Step 1: Creating datafile.h5 ... ---")
    start_time = time.time()
    if args.chr_split == 'test':
        print("Creating test datafile...")
        get_sequences_and_labels(db, args.genome_fasta, args.output_dir, seq_dict, data_type="test", chrom_dict=TEST_CHROM_GROUP, parse_type=args.parse_type, biotype=args.biotype)
    elif args.chr_split == 'train-test':
        print("Creating train datafile...")
        get_sequences_and_labels(db, args.genome_fasta, args.output_dir, seq_dict, data_type="train", chrom_dict=TRAIN_CHROM_GROUP, parse_type=args.parse_type, biotype=args.biotype)
        print("Creating test datafile...")
        get_sequences_and_labels(db, args.genome_fasta, args.output_dir, seq_dict, data_type="test", chrom_dict=TEST_CHROM_GROUP, parse_type=args.parse_type, biotype=args.biotype)
    utils.print_motif_counts(donor_motif_counts, acceptor_motif_counts)
    print("--- %s seconds ---" % (time.time() - start_time))