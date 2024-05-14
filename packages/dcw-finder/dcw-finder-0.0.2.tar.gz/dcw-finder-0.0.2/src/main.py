import time
import subprocess
import os

from _utils import sum_assembly_report
from _utils import organize_input_dir
from _parse import parse_genome
from _blast import run_blastp
from _count import count_blastp_result
from _seqlib import create_seqlib
from _search import search_target
from _count import count_mmseq_result
from _cluster import cluster_target
from _cluster import classify_cluster_type
from _accessory import collect_accessory
from _profile import final_profile
from _target import process_target_data

def find_gene_cluster(TAXON, target_path):
    if not os.path.exists(target_path):
        print("<< Target file does not exist. Please provide a valid file path.")
        return

    start_time = time.time()

    subprocess.run(['bash', './init.sh', TAXON])

    project_info = {
            'project_name': TAXON + " gene cluster",
            'root': f"../{TAXON}",
            'input': f"../{TAXON}/input",
            'output': f"../{TAXON}/output",
            'data': f"../{TAXON}/data",
            'seqlib': f"../{TAXON}/seqlib"
            }

    input_len = sum_assembly_report(project_info)
    project_info['input_len'] = input_len
    organize_input_dir(project_info)
    parse_genome(project_info)

    process_target_data(project_info, target_path)
    run_blastp(project_info)
    count_blastp_result(project_info)

    create_seqlib(project_info)
    search_target(project_info)
    count_mmseq_result(project_info)

    cluster_target(project_info)
    classify_cluster_type(project_info)

    collect_accessory(project_info)
    final_profile(project_info)

    end_time = time.time()
    total = end_time - start_time
    print("------------------------------------------")
    print(f"<< ALL DONE (elapsed time: {round(total / 60, 3)} min)")
    print("------------------------------------------")

TAXON = input(">> Enter TAXON value: ")
target_path = input(">> Enter target file path: ")
find_gene_cluster(TAXON, target_path)