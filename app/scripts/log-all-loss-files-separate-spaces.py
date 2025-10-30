#!/usr/bin/env python3
"""
Script pour créer un Space Trackio par projet de loss
Utilise l'API Hugging Face Hub pour créer des Spaces séparés
"""

import trackio
import pandas as pd
import sys
from pathlib import Path
from huggingface_hub import HfApi, SpaceCard

def get_project_space_id(project_name):
    """Génère un space_id unique pour chaque projet"""
    username = "tfrere"  # Ton username Hugging Face
    space_name = f"loss-{project_name.replace('-', '-').lower()}"
    return f"{username}/{space_name}"

def create_space_if_needed(space_id):
    """Crée un Space s'il n'existe pas déjà"""
    api = HfApi()
    
    try:
        # Vérifier si le Space existe
        api.space_info(space_id)
        print(f"  ✅ Space existant: {space_id}")
        return space_id
    except Exception:
        # Créer le nouveau Space
        try:
            print(f"  🆕 Création du Space: {space_id}")
            # Le Space sera créé automatiquement par Trackio lors du premier init
            return space_id
        except Exception as e:
            print(f"  ⚠️ Erreur lors de la création du Space: {e}")
            return space_id

def log_loss_file_to_trackio(data_file, project_name=None):
    """Log un fichier de loss vers Trackio avec son propre Space"""
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
        
        # Déterminer le nom du projet et son Space
        if project_name is None:
            # Extraire le nom du fichier et créer un nom de projet
            base_name = data_file.stem.replace('_loss', '').replace('_', '-')
            project_name = f"{base_name}-comparison"
        
        space_id = get_project_space_id(project_name)
        print(f"🎯 Projet Trackio: {project_name}")
        print(f"🌐 Space ID: {space_id}")
        
        # Créer le Space si nécessaire
        create_space_if_needed(space_id)
        
        # Logger chaque run dans le MÊME projet
        for i, run_name in enumerate(runs):
            print(f"\n🌐 Création du run: \"{run_name}\"")
            
            # Initialiser Trackio avec le même projet mais son propre Space
            trackio.init(
                project=project_name, 
                space_id=space_id,  # Space unique pour ce projet
                name=run_name,
                resume="allow"
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
        
        print(f"\n🎉 Projet {project_name} créé avec {len(runs)} runs dans Space {space_id}!")
        return True, space_id
        
    except Exception as e:
        print(f"❌ Erreur lors du logging de {data_file.name}: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    print("🎯 Logger tous les fichiers de loss vers Trackio")
    print("=" * 60)
    print("🔄 Un Space Trackio par projet de loss")
    print("=" * 60)
    
    # Liste des fichiers à traiter
    data_dir = Path("src/content/assets/data")
    
    # Mapping fichier -> nom de projet
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
    
    # Traiter chaque fichier et stocker les space_ids
    results = {}
    space_ids = {}
    
    for filename, project_name in file_mappings.items():
        data_file = data_dir / filename
        if data_file.exists():
            success, space_id = log_loss_file_to_trackio(data_file, project_name)
            results[filename] = success
            if success:
                space_ids[project_name] = space_id
        else:
            print(f"\n⚠️ Fichier non trouvé: {filename}")
            results[filename] = False
    
    # Résumé avec les URLs des Spaces
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print("\n✅ Projets créés avec leurs Spaces:")
    for filename, success in results.items():
        if success:
            project_name = file_mappings[filename]
            space_id = space_ids.get(project_name, "N/A")
            status = "✅"
            print(f"{status} {filename:30s} → {space_id}")
    
    print(f"\n🎉 {success_count}/{total_count} fichiers loggés avec succès!")
    print(f"\n🌐 URLs des Spaces:")
    for project_name, space_id in space_ids.items():
        print(f"  - {project_name}: https://huggingface.co/spaces/{space_id}")
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    exit(main())
