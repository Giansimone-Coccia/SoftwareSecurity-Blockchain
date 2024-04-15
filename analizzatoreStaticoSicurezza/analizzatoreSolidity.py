import subprocess
import os

def run_slither_on_directory():
    # Comando per eseguire Slither sulla directory corrente
    slither_command = ['slither', '.']

    script_path = os.path.abspath(__file__)
    
    # Estrai la directory dello script
    script_directory = os.path.dirname(script_path)
    output_file_path = os.path.join(script_directory, "risultati_analisi_slither.txt")
    result = subprocess.run(slither_command, capture_output=True, text=True)
    
    # Scrivi l'output su un file di testo
    with open(output_file_path, 'w+') as file:
        file.write("Return code: {}\n\n".format(result.returncode))
        file.write("Standard Output:\n")
        file.write(result.stdout)
        file.write("\n\nStandard Error:\n")
        file.write(result.stderr)
    
    print("Output di Slither salvato in 'risultati_analisi_slither.txt'")

# Esegui Slither sulla directory corrente e salva l'output in un file di testo
run_slither_on_directory()
