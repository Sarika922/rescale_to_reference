rule all:
    input:
        "rescale_to_reference",
        "output/query_subsampled_plot.png"

rule load_reference_distribution:
    input:
        "reference.hist"
    output:
        "reference_normalized.txt"
    run:
        import pandas as pd

        ref_data = pd.read_csv(input[0], sep="\t", header=None, names=["FragmentLength", "Frequency"])
        max_ref_freq = ref_data["Frequency"].max()
        ref_data["NormalizedFrequency"] = ref_data["Frequency"] / max_ref_freq
        ref_data.to_csv(output[0], sep="\t", index=False)

rule load_query_distribution:
    input:
        "shuf.a.bed.gz"
    output:
        "query_distribution.txt"
    shell:
        """
        zcat {input} | awk '{{print $3 - $2}}' | sort | uniq -c | \
        awk '{{print $2, $1}}' | \
        awk '{{total += $2; data[$1] = $2}} END {{for (len in data) print len, data[len], data[len]/total}}' > {output}
        """

rule subsample_query:
    input:
        query="query_distribution.txt",
        reference="reference_normalized.txt"
    output:
        plot="output/query_subsampled_plot.png"
    script:
        "scripts/subsample_and_plot.py"
