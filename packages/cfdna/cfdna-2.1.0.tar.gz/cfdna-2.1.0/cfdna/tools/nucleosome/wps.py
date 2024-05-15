import ngsfragments as ngs
import numpy as np
import pandas as pd
from ailist import LabeledIntervalArray
import scipy


def wps(frags, chrom=None, protection=120, min_length=120, max_length=210, normalize=True, norm_method="mean"):
    """
    Calculate Window Protection Score (WPS)

    Parameters
    ----------
        frags : ngsfragments.fragments
            Fragments object
        chroms : str or list
            Name of chromosome
        protection : int
            Protection window
        min_length : int
            Minimum DNA fragment length
        max_length : int
            Maximum fragment length
        normalize : bool
            Whether to normalize
        norm_method : str
            Normalization method

    Returns
    -------
        wps_score : pandas.Series
            Window protection scores
    """
    
    # Caclulate WPS
    wps_score = frags.wps(chrom=chrom, protection=protection, min_length=min_length, max_length=max_length)
    if normalize:
        ngs.utilities.normalize_wps(wps_score, method=norm_method)

    return wps_score


def coverage(frags, chrom=None, min_length=120, max_length=210, normalize=True, norm_method="mean"):
    """
    Calculate Window Protection Score (WPS)

    Parameters
    ----------
        frags : ngsfragments.fragments
            Fragments object
        chroms : str or list
            Name of chromosome
        min_length : int
            Minimum DNA fragment length
        max_length : int
            Maximum fragment length
        normalize : bool
            Whether to normalize
        norm_method : str
            Normalization method

    Returns
    -------
        cov : pandas.Series
            Coverage
    """
    
    # Caclulate coverage
    cov = frags.coverage(chrom=chrom, min_length=min_length, max_length=max_length)
    if normalize:
        ngs.utilities.normalize_wps(cov, method=norm_method)

    return cov


def predict_nucleosomes(self,
                        fragments,
                        protection = 120,
                        merge_distance = 5,
				        min_length = 120,
                        max_length = 500,
                        verbose = False):
    """
    Call peaks from WPS

    Parameters
    ----------
        chrom
            str (chromosomes to call for)

    Returns
    -------
        peaks
            dict[chrom:AIList] (WPS peaks)
    """

    # Iterate over chromosomes
    chroms = fragments.frags.unique_labels

    # Initialize peaks
    total_peaks = LabeledIntervalArray()

    # Iterate over chromosomes
    for chrom in chroms:
        if verbose: print(chrom, flush=True)
        wps = fragments.frags.wps(protection, chrom, min_length, max_length)
        wps[chrom].values[:] = ngs.peak_calling.CallPeaks.normalize_signal(wps[chrom].values)

        peaks = ngs.peak_calling.CallPeaks.call_peaks(wps[chrom], str(chrom), merge_distance, 50, 190)
        if peaks.size < 10:
            continue
        midpoints = (peaks.starts + ((peaks.ends - peaks.starts) / 2)).astype(int)
        standard_peaks = LabeledIntervalArray()
        standard_peaks.add(midpoints - 84, midpoints + 84, np.repeat(chrom, len(midpoints)))
        standard_peaks = standard_peaks.merge()
        midpoints = (standard_peaks.starts + ((standard_peaks.ends - standard_peaks.starts) / 2)).astype(int)
        standard_peaks = LabeledIntervalArray()
        standard_peaks.add(midpoints - 84, midpoints + 84, np.repeat(chrom, len(midpoints)))
        total_peaks.append(standard_peaks)

    return total_peaks


def merge_nucleosomes(peaks1, peaks2, merge_distance=10):
    """
    Merge two sets of nucleosomes

    Parameters
    ----------
        peaks1
            dict[chrom:AIList]
        peaks2
            dict[chrom:AIList]
        merge_distance
            int

    Returns
    -------
        merged_peaks
            dict[chrom:AIList]
    """

    # Merge peaks
    merged_peaks = peaks1.union(peaks2).merge(merge_distance)
    
    # Re-center peaks
    midpoints = (merged_peaks.starts + ((merged_peaks.ends - merged_peaks.starts) / 2)).astype(int)
    standard_peaks = LabeledIntervalArray()
    standard_peaks.add(midpoints - 84, midpoints + 84, merged_peaks.labels)

    return standard_peaks


def internucleosomal_distances(peaks, max_distance=1000):
    """
    Determine distance between nucleosomes
    """

    # Iterate over chromosomes
    chroms = peaks.unique_labels

    # Initialize distances
    distances = []

    # Iterate over chromosomes
    for chrom in chroms:
        chrom_peaks = peaks.get(chrom)
        midpoints = (chrom_peaks.starts + ((chrom_peaks.ends - chrom_peaks.starts) / 2)).astype(int)

        pdist = np.diff(midpoints)
        distances.extend(pdist[pdist < max_distance])

    distances = np.array(distances)

    return distances


def peak_distances(self, fragments, peaks=None, bin_size=100000, max_distance=10000):
    """
    Determine distance between peaks

    Parameters
    ----------
        peaks
            dict[chrom:AIList]
        bin_size
            int
        max_distance
            int
        smooth
            bool

    Returns
    -------
        peak_bins
            dict[pandas.Series]
    """

    # Calculate peaks
    if peaks is None:
        peaks = self.predict_nucleosomes(fragments)

    # Create p_dist IntervalFrame
    starts = np.array([],dtype=int)
    chroms = np.array([], dtype="U25")
    for chrom in peaks:
        new_starts = np.arange(0, self.chrom_sizes[chrom]+bin_size, bin_size)
        starts = np.append(starts, new_starts)
        chroms = np.append(chroms, np.repeat(chrom, len(new_starts)))
    ends = starts + bin_size
    p_dist = IntervalFrame.from_array(starts, ends, labels=chroms)

    # Iterate over intervals
    p_dist.df.loc[:,"mean_dist"] = 0
    for i, interval in enumerate(p_dist.index):
        chrom = interval.label
        try:
            peaks[chrom]
            overlaps = peaks[chrom].intersect(interval.start, interval.end, label=chrom)
            if len(overlaps) > 3:
                p_dist.df.loc[i,"mean_dist"] = np.mean(overlaps.extract_ends()[:-1] - overlaps.extract_starts()[1:])
        except KeyError:
            pass

    # Remove those greater than max_distance
    p_dist = p_dist.iloc[p_dist.df.loc[:,"mean_dist"].values < max_distance, :]

    return p_dist


def wps_gene_fft(fragments,
                 genome_version = "hg38",
                 protection = 120,
				 min_length = 120,
                 max_length = 500,
                 verbose = False):
    """
    """

    import genome_info

    genome = genome_info.GenomeInfo(genome_version)
    genes = genome.get_intervals("tss", downstream=10000, filter_column="gene_type", filter_selection="protein_coding")

    # Iterate over chromosomes
    chroms = fragments.frags.unique_labels

    # Initialize scores
    scores = pd.DataFrame(np.zeros((genes.shape[0], 1000)), index=genes.loc[:,"gene_name"].values)

    # Iterate over chromosomes
    k = 0
    for chrom in chroms:
        if verbose: print(chrom, flush=True)
        wps = fragments.frags.wps(protection, chrom, min_length, max_length)
        wps[chrom].values[:] = ngs.peak_calling.CallPeaks.normalize_signal(wps[chrom].values)

        chrom_genes = genes.loc[chrom,:]

        for i in range(chrom_genes.shape[0]):
            interval = chrom_genes.index[i]
            if len(wps[chrom].loc[interval.start:interval.end-2].values) == 10000:
                values = wps[chrom].loc[interval.start:interval.end-2].values
                values = ngs.correct.correction.gaussian_smooth(values, 10)
                values = values - np.mean(values)
                values = scipy.signal.detrend(values)
                #sos = scipy.signal.butter(5,100, btype="highpass", fs=10000, output="sos")
                #values = scipy.signal.sosfilt(sos, values)
                values = scipy.fftpack.fft(values)
                scores.iloc[k,:] = np.abs(values)[:1000]
            k += 1


    #scores.values[chrom_genes.loc[:,"Strand"].values == "-",:] = scores.values[chrom_genes.loc[:,"Strand"].values == "-",:][:,::-1]

    #n = ((scores.T - scores.min(axis=1).values) / (scores.max(axis=1).values - scores.min(axis=1).values)).T
    #n = n.loc[np.sum(pd.isnull(n), axis=1).values == 0,:]

    #x = np.fft.fft2(n.values)
    #x = np.fft.fftshift(x)

    #expr = pd.Series(x[:,193:200].mean(axis=1).astype(float), scores.index.values)

    return scores