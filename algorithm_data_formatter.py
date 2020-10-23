from datetime import datetime

is_record_genome = True


def get_date_time_now():
    now = datetime.now()
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")


def algorithm_analysis_data_schema(genome, strain, gLength, dLength, genome_file_type, time_executed, method,
                                   comparison, positions):
    if is_record_genome:
        data = {
            "genome": genome,
            "genome_length": gLength,
            "dna_strain": strain,
            "dna_strain_length": dLength,
            "genome_file_type": genome_file_type,
            "time_executed": time_executed,
            "method": method,
            "comparison": comparison,
            "matches": len(positions),
            "path found": positions
        }
    else:
        data = {
            "genome": "fna file",
            "genome_length": gLength,
            "dna_strain": strain,
            "dna_strain_length": dLength,
            "genome_file_type": "fna",
            "time_executed": time_executed,
            "method": method,
            "comparison": comparison,
            "matches": len(positions),
            "position found": positions
        }
    return data
