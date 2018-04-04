#!/zzh_gpfs/apps/python/bin/python
import os,sys,csv
from Bio import SeqIO
import argparse

def main():
	fasta_dict = SeqIO.index(infasta,'fasta')
	inf1 = open(infile,'rU')
	out = csv.writer(open('%s/%s'%(outdir,outname),'wb'),delimiter='\t')
	igblast_dict = {}
	myid = ""
	for rec in inf1:
		if rec.startswith("# Query:"):
			if len(myid)!=0:
				if len(Vinfo)>0 and len(Jinfo)>0:
					variable_seq = str(myseq1.seq[int(Vinfo[8])-1:int(Jinfo[9])])
					V_seq = str(myseq1.seq[int(Vinfo[8])-1:int(Vinfo[9])])
					if len(cdr3)>0:
						out.writerow([cdr3[1],cdr3[2],myid,";".join(recom),";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),variable_seq,V_seq])
					else:
						out.writerow(["N/A","N/A",myid,";".join(recom),";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),variable_seq,V_seq])
			myid,recom,cdr3,Vinfo,Dinfo,Jinfo = "",[],[],[],[],[]
			myid = rec.strip().split(" ")[2]
			vnum, dnum, jnum = 0,0,0
		elif rec.startswith("IG"):
			info = rec.strip().split("\t")
			if len(info)==8:
				recom = info
			elif len(info)==7:
				recom = [info[0],"N/A"]+info[1:]
		elif rec.startswith("TR"):
			info = rec.strip().split("\t")
			if len(info)==8:
				recom = info
			elif len(info)==7:
				recom = [info[0],"N/A"]+info[1:]
		elif rec.startswith("CDR3\t"):
			cdr3 = rec.strip().split("\t")
		elif rec.startswith("V\t") and vnum==0:
			Vinfo = rec.strip().split("\t")
			if Vinfo[1].startswith("reversed"):
				myseq1 = fasta_dict[myid].reverse_complement()
			else:
				myseq1 = fasta_dict[myid]
			vnum = 1
		elif rec.startswith("D\t") and dnum==0:
			Dinfo = rec.strip().split("\t")
			dnum = 1
		elif rec.startswith("J\t") and jnum==0:
			Jinfo = rec.strip().split("\t")
			jnum = 1
	variable_seq = str(myseq1.seq[int(Vinfo[8])-1:int(Jinfo[9])])
	V_seq = str(myseq1.seq[int(Vinfo[8])-1:int(Vinfo[9])])
	if len(Vinfo)>0 and len(Jinfo)>0:
		variable_seq = str(myseq1.seq[int(Vinfo[8])-1:int(Jinfo[9])])
		V_seq = str(myseq1.seq[int(Vinfo[8])-1:int(Vinfo[9])])
		if len(cdr3)>0:
			out.writerow([cdr3[1],cdr3[2],myid,";".join(recom),";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),variable_seq,V_seq])
		else:
			out.writerow(["N/A","N/A",myid,";".join(recom),";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),variable_seq,V_seq])
	
if __name__=='__main__':
	parser = argparse.ArgumentParser(prog='python ParseIgBLAST.py',usage='%(prog)s -f fasta -i igblast -o outname -d outdir',description = 'Parse IgBLAST result, and get CDR3_nt, CDR3_aa, ID, recombination_info, Vinfo, Dinfo, Jinfo, variable_seq, V_seq, etc',epilog = 'Created by WangCR. April 2, 2018')
	parser.add_argument('-f','--fasta',help='Input fasta format file')
	parser.add_argument('-i','--igblast',help='Input igblast m7 format result')
	parser.add_argument('-d','--outdir',default=".",help='Output file director')
	parser.add_argument('-o','--outfile',default="result.txt",help='Output tab format file, which record search results.')
	parser.add_argument('-v','--version', action='version', version='Copyright (c) 31/3/2018, created by WangChengrui, version 1.0')
	args = parser.parse_args()
	infasta = args.fasta
	infile = args.igblast
	outdir = args.outdir
	outname = args.outfile
	os.system("mkdir -p %s"%outdir)
	main()
