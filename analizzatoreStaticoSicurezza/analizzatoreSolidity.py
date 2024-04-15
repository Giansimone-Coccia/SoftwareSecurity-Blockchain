import subprocess

def run_slither_on_directory():
    # Comando per eseguire Slither sulla directory corrente
    slither_command = ['slither', '.']

    result = subprocess.run(slither_command, capture_output=True, text=True)
    
    # Scrivi l'output su un file di testo
    with open('/Users/lauraferretti/Documents/SoftwareSecurity-Blockchain/analizzatoreStaticoSicurezza/risultati_analisi_slither.txt', 'w') as file:
        file.write("Output di Slither:\n\n")
        file.write("Return code: {}\n\n".format(result.returncode))
        file.write("Standard Output:\n")
        file.write(result.stdout)
        file.write("\n\nStandard Error:\n")
        file.write(result.stderr)
    
    print("Output di Slither salvato in 'risultati_analisi_slither.txt'")

# Esegui Slither sulla directory corrente e salva l'output in un file di testo
run_slither_on_directory()
