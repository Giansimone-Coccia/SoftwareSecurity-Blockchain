import os
import subprocess
import glob

def run_bandit_on_files(directory, output_file, exclude_folders=None):
    # Ottieni il percorso completo dello script attuale
    script_path = os.path.abspath(__file__)
    
    # Estrai la directory dello script
    script_directory = os.path.dirname(script_path)
    
    # Lista di tutti i file Python nella directory (e nelle sotto-directory)
    python_files = glob.glob(os.path.join(directory, '**/*.py'), recursive=True)
    
    # Comando per eseguire Bandit su ciascun file Python
    bandit_command = ['bandit']

    # Esegui Bandit su ciascun file e salva l'output
    output_file_path = os.path.join(script_directory, output_file)
    with open(output_file_path, 'w') as output:
        for file in python_files:
            # Escludi il file dello script e le cartelle specificate
            exclude = False
            if os.path.basename(file) != os.path.basename(script_path):
                if exclude_folders:
                    for folder in exclude_folders:
                        if folder in os.path.abspath(file):
                            exclude = True
                            break
                if not exclude:
                    print(f"FILE ANALIZZATO    ---->    {os.path.basename(file)}  ")
                    bandit_command.append(file)
                    result = subprocess.run(bandit_command, capture_output=True, text=True)
                    output.write(f"Risultati per il file: {file}\n")
                    output.write(result.stdout)
                    output.write("\n\n")
                    bandit_command.pop()  # Rimuovi il file aggiunto per l'esecuzione successiva

    print("Risultati salvati in:", output_file_path)

# Directory da analizzare e file in cui salvare i risultati
directory_da_analizzare = os.getcwd()
file_risultati = 'risultati_analisi.txt'

# Cartelle da escludere
cartelle_da_escludere = ['analizzatoreStaticoSicurezza', 'contracts', 'solidityContracts', 'test']

# Esegui Bandit su tutti i file Python nella directory e salva i risultati
run_bandit_on_files(directory_da_analizzare, file_risultati, exclude_folders=cartelle_da_escludere)
