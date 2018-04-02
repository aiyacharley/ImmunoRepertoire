"""
usage:
	python *.py /path/to/data/dir/
"""
import os,sys,csv
import subprocess
from multiprocessing import Pool, Process, Manager
from glob import glob
import Bio
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def batch_iterator(iterator, batch_size) :
	"""Returns lists of length batch_size.

	This can be used on any iterator, for example to batch up
	SeqRecord objects from Bio.SeqIO.parse(...), or to batch
	Alignment objects from Bio.AlignIO.parse(...), or simply
	lines from a file handle.

	This is a generator function, and it returns lists of the
	entries from the supplied iterator.  Each list will have
	batch_size entries, although the final list may be shorter.
	"""
	entry = True
	while entry :
		batch = []
		while len(batch) < batch_size :
			try :
				entry = iterator.next()
			except StopIteration :
				entry = None
			if entry is None :
				break
			batch.append(entry)
		if batch:
			yield batch

def trim_fastq_by_quality(the_file):
	handle = open(the_file, "rU")
	print "Triming...%s"%the_file
	trim_file = "merge.assembled_trimed.fastq"
	writer = open(trim_file, "w")
	for ind,record in enumerate(SeqIO.parse(handle, "fastq")):
		if (ind+1)%100000 == 0:
			print "%d recods trimed ... "%(ind+1)
		quality_type = list(record.letter_annotations)[0]
		quality_list = record.letter_annotations[quality_type]
		position_list = []
		for index in range(0,len(quality_list)):
			if quality_list[index] > 20:
				position_list.append(index)
		new_record = record[position_list[0] : position_list[-1]+1]
		SeqIO.write(new_record, writer, "fastq")
	handle.close()
	writer.close()

def change_ID_name(fasta_old):
	file_old = SeqIO.parse(fasta_old, 'fasta')
	outfile = open('merge.assembled_trimed.fasta',"w")
	index = 1
	for record in file_old:
		new_record = SeqRecord(record.seq, id = "%08d-M"%(index), description = '')
		index += 1
		SeqIO.write(new_record, outfile, "fasta")
	outfile.close()

def split_to_subfiles(fasta_iteror):
	for i, batch in enumerate(batch_iterator(fasta_iteror, 5000)):
		filename = "merge_%i.fasta" % (i+1)
		handle = open(filename, "w")
		count = SeqIO.write(batch, handle, "fasta")
		handle.close()
		print "Wrote %i records to %s" % (count, filename)

def merge_trim_convert2fasta_subfile_igblast(sample_fold):
	os.chdir(sample_fold)
	print "1. PEAR merging ... "
	fastq_pair = glob('*.fastq*')
	merge = subprocess.call("pear -j 4 -q 20 -f %s -r %s -o merge"%(fastq_pair[0],fastq_pair[1]),shell=True)
	if os.path.getsize("merge.assembled.fastq")==0:
		merge = subprocess.call("flash %s %s"%(fastq_pair[0],fastq_pair[1]),shell=True)
		os.system("mv out.extendedFrags.fastq merge.assembled.fastq")

	print "2. Trim QC20 ... "
	trim_fastq_by_quality('merge.assembled.fastq')

	print "3. Convert2fasta ... "
	count = SeqIO.convert('merge.assembled_trimed.fastq',"fastq","merge.assembled_trimed.fasta","fasta")
	print "There are  %i records have been Converted!" %(count)

	print "4. Change ID name ... "
	os.system("mv merge.assembled_trimed.fasta merge.assembled_trimed.fasta.old_name")
	change_ID_name('merge.assembled_trimed.fasta.old_name')

	#print "5. Split to subfile ... "
	#fasta_iteror = SeqIO.parse(open("merge.assembled_trimed.fasta"),"fasta")
	#os.system('mkdir fasta_subfiles')
	#os.chdir('%s/fasta_subfiles'%sample_fold)
	#split_to_subfiles(fasta_iteror)

def process_sample(data_fold):
	merge_trim_convert2fasta_subfile_igblast(data_fold)
	
def main():
	process_sample(data_fold)

if __name__ == '__main__':
	data_fold = sys.argv[1]  ### data fold path , /path/to/data/
	main()
	print "2.0-Merge-Split-IgBLAST.py done !!! "
