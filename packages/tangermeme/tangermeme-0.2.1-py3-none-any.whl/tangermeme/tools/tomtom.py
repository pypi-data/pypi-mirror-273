# tomtom.py
# Contact: Jacob Schreiber <jmschreiber91@gmail.com> 

import numpy
import torch

from ..io import read_meme
from ..predict import predict

from .fimo import FIMO


class TOMTOM(FIMO):
	"""A method for comparing candidate PWMs against a database of PWMs.

	TOMTOM is a method for comparing sequences, or even entire PWMs, against a
	database of known PWMs and returning hits. This is useful when you have
	a candidate sequence that is thought to be important in some manner and
	you want to compare it against a candidate list of known protein binding
	sites.

	This is implemented as a wrapper of FIMO, where the candidate sequences are
	being scanned over by a database of motifs and the maximum score from the
	database is returned for each sequence.


	Parameters
	----------
	motifs: str or dict
		Either a filename to a set of motifs in MEME format or a dictionary
		where the keys are names of motifs and the values are 

	n_motifs: int or None, optional
		Limit the database to the first `n_motifs` entires. Useful for
		debugging. If None, use all motifs. Default is None.
	"""

	def __init__(self, motifs, alphabet=['A', 'C', 'G', 'T'], batch_size=256, 
		bin_size=0.1, eps=0.00005):
		super().__init__()
		self.bin_size = bin_size
		self.alphabet = numpy.array(alphabet)

		if isinstance(motifs, str):
			motifs = read_meme(motifs)
			
		self.motif_names = numpy.array([name for name in motifs.keys()])
		self.motif_lengths = numpy.array([len(motif) for motif in 
			motifs.values()])
		self.n_motifs = len(self.motif_names)
		self.max_length = max(self.motif_lengths)
		self.sum_length = sum(self.motif_lengths)

		self.motifs = torch.cat([motif for motif in motifs.values()], dim=0).T
		

	def forward(self, X, n_bins=100):
		for i in range(X.shape[0]):
			score = X[i].T.dot(self.motifs)
			smallest, largest = score.min(), score.max()

			score = (score - smallest) / (largest - smallest) * n_bins
			score = torch.round(score)

			bg = torch.zeros(X.shape[-1], n_bins+1)
			bg.scatter_add_(1, score, torch.ones(1).expand_as(score))
			bg = bg.mean(axis=0)

			print(bg)


			A = torch.zeros(X.shape[-1], n_bins+1)
			A[:, 0] = 1

			for j in range(1, X.shape[-1]):
				for k in range(n_bins+1):
					for l in range(n_bins+1):
						A[j, l] += A[j-1, k-l] * bg[j, k]
				
			
			



			




			A = torch.zeros(X.shape[-1], self.sum_length, dtype=X.dtype, 
				device=X.device)





	def hits(self, X):
		return self(X)