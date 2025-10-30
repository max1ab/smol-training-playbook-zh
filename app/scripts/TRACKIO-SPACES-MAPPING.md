# Mapping des projets Trackio vers leurs Spaces

Ce fichier liste tous les projets Trackio et leurs Space IDs correspondants pour éviter le flooding quand plusieurs embeds sont affichés.

## Projets et leurs Spaces

| Projet | Space ID | URL |
|--------|----------|-----|
| attention-loss-comparison | tfrere/loss-attention-loss-comparison | https://huggingface.co/spaces/tfrere/loss-attention-loss-comparison |
| batch-size-loss-comparison | tfrere/loss-batch-size-loss-comparison | https://huggingface.co/spaces/tfrere/loss-batch-size-loss-comparison |
| doc-masking-loss-comparison | tfrere/loss-doc-masking-loss-comparison | https://huggingface.co/spaces/tfrere/loss-doc-masking-loss-comparison |
| lr-loss-comparison | tfrere/loss-lr-loss-comparison | https://huggingface.co/spaces/tfrere/loss-lr-loss-comparison |
| nope-loss-comparison | tfrere/loss-nope-loss-comparison | https://huggingface.co/spaces/tfrere/loss-nope-loss-comparison |
| spike-loss-comparison | tfrere/loss-spike-loss-comparison | https://huggingface.co/spaces/tfrere/loss-spike-loss-comparison |
| tied-embeddings-loss-comparison | tfrere/loss-tied-embeddings-loss-comparison | https://huggingface.co/spaces/tfrere/loss-tied-embeddings-loss-comparison |
| tp-debug-fix-loss-comparison | tfrere/loss-tp-debug-fix-loss-comparison | https://huggingface.co/spaces/tfrere/loss-tp-debug-fix-loss-comparison |
| wsd-loss-comparison | tfrere/loss-wsd-loss-comparison | https://huggingface.co/spaces/tfrere/loss-wsd-loss-comparison |

## Utilisation dans l'article

Pour chaque projet, utilise son Space ID spécifique dans l'iframe :

```html
<!-- Attention Loss -->
<iframe 
  src="https://tfrere-loss-attention-loss-comparison.hf.space?project=attention-loss-comparison&metrics=loss&sidebar=hidden&navbar=hidden&xmin=0&xmax=40&smoothing=0" 
  style="width:100%; height:350px; border:0;">
</iframe>

<!-- Batch Size Loss -->
<iframe 
  src="https://tfrere-loss-batch-size-loss-comparison.hf.space?project=batch-size-loss-comparison&metrics=loss&sidebar=hidden&navbar=hidden&xmin=0&xmax=40&smoothing=0" 
  style="width:100%; height:350px; border:0;">
</iframe>
```

## Avantages

✅ **Pas de flooding** : Chaque embed utilise son propre Space
✅ **Meilleure performance** : Les requêtes sont distribuées
✅ **Isolation** : Chaque projet est indépendant
✅ **Scalabilité** : Facile d'ajouter de nouveaux projets

## Notes

- Les Spaces seront créés automatiquement lors du premier `trackio.init()`
- Chaque Space a son propre dataset Hugging Face
- Les Spaces sont publics par défaut (configurable dans le script)
