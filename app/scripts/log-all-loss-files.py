#!/usr/bin/env python3
"""
Script générique pour logger n'importe quel fichier de loss vers Trackio
Un projet Trackio par fichier de loss
"""

import trackio
import pandas as pd
import sys
from pathlib import Path

def get_project_name_from_file(filename):
    """Convertit un nom de fichier en nom de projet Trackio"""
    # Enlever l'extension et les tirets, remplacer par des tirets simples
    project = filename.replace('_loss.csv', '').replace('_', '-').replace('.csv', '')
    return f"{project}-comparison"

def log_loss_file_to_trackio(data_file, project_name=None):
    """Log un fichier de loss vers Trackio"""
    print(f"\n🚀 Traitement de: {data_file.name}")
    
    if not data_file.exists():
        print(f"❌ Fichier non trouvé: {data_file}")
        return False
    
    try:
        # Charger les données
        df = pd.read_csv(data_file)
        print(f"📁 Données chargées: {len(df)} lignes")
        
        # Obtenir les runs uniques
        if 'run_name' not in df.columns:
            print(f"❌ Pas de colonne 'run_name' dans {data_file.name}")
            return False
            
        runs = df['run_name'].unique()
        print(f"🔍 Runs à créer ({len(runs)}):")
        for run in runs:
            count = len(df[df['run_name'] == run])
            print(f'  - "{run}": {count} points')
        
        # Déterminer le nom du projet
        if project_name is None:
            project_name = get_project_name_from_file(data_file.name)
        print(f"🎯 Projet Trackio: {project_name}")
        
        # Logger chaque run dans le MÊME projet
        for i, run_name in enumerate(runs):
            print(f"\n🌐 Création du run: \"{run_name}\"")
            
            # Initialiser Trackio avec le même projet
            trackio.init(
                project=project_name, 
                space_id="tfrere/loss-experiment",
                name=run_name,
                resume="allow"  # Permettre de reprendre ou créer un nouveau run
            )
            
            # Filtrer les données pour ce run
            run_data = df[df['run_name'] == run_name]
            print(f"📊 Logging de {len(run_data)} points...")
            
            # Logger les données de ce run
            for j, (_, row) in enumerate(run_data.iterrows()):
                log_data = {
                    "loss": float(row['loss'])
                }
                
                # Utiliser tokens comme axe X principal si disponible
                if 'tokens' in row:
                    log_data["tokens"] = float(row['tokens'])
                else:
                    # Sinon utiliser un compteur de step
                    log_data["step"] = j
                
                trackio.log(log_data)
                
                if j % 100 == 0 and j > 0:
                    print(f"  ✅ Étape {j}/{len(run_data)}")
            
            # Finaliser ce run
            trackio.finish()
            print(f"✅ Run \"{run_name}\" terminé!")
        
        print(f"\n🎉 Projet {project_name} créé avec {len(runs)} runs!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du logging de {data_file.name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🎯 Logger tous les fichiers de loss vers Trackio")
    print("=" * 60)
    print("🔄 Un projet Trackio par fichier de loss")
    print("=" * 60)
    
    # Liste des fichiers à traiter
    data_dir = Path("src/content/assets/data")
    
    # Mapping fichier -> nom de projet (optionnel, sinon généré automatiquement)
    file_mappings = {
        "attention_loss.csv": "attention-loss-comparison",
        "batch-size_loss.csv": "batch-size-loss-comparison",
        "doc-masking_loss.csv": "doc-masking-loss-comparison",
        "lr_loss.csv": "lr-loss-comparison",
        "nope_loss.csv": "nope-loss-comparison",
        "spike_loss.csv": "spike-loss-comparison",
        "tied-embeddings_loss.csv": "tied-embeddings-loss-comparison",
        "tp_debug_fix_loss.csv": "tp-debug-fix-loss-comparison",
        "wsd_loss.csv": "wsd-loss-comparison",
    }
    
    # Traiter chaque fichier
    results = {}
    for filename, project_name in file_mappings.items():
        data_file = data_dir / filename
        if data_file.exists():
            results[filename] = log_loss_file_to_trackio(data_file, project_name)
        else:
            print(f"\n⚠️ Fichier non trouvé: {filename}")
            results[filename] = False
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for filename, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {filename}")
    
    print(f"\n🎉 {success_count}/{total_count} fichiers loggés avec succès!")
    print(f"📊 Consultez votre dashboard: https://huggingface.co/spaces/tfrere/loss-experiment")
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    exit(main())
