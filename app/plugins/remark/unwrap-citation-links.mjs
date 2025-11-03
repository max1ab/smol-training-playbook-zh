// Plugin remark pour transformer les liens markdown contenant des citations en citations simples
// Transforme [@reference](url) en [@reference]
export default function remarkUnwrapCitationLinks() {
    return (tree) => {
        // Fonction helper pour extraire le contenu textuel d'un nœud
        const getTextContent = (node) => {
            if (!node) return '';
            if (node.type === 'text') return node.value || '';
            if (Array.isArray(node.children)) {
                return node.children.map(getTextContent).join('');
            }
            return '';
        };

        const visit = (node, parent) => {
            if (!node || typeof node !== 'object') return;

            // Parcourir les enfants d'abord (post-order traversal)
            const children = Array.isArray(node.children) ? node.children : [];
            for (let i = 0; i < children.length; i++) {
                const child = children[i];
                visit(child, node);
            }

            // Si c'est un nœud de type 'link', vérifier son contenu
            if (node.type === 'link' && parent && Array.isArray(parent.children)) {
                // Récupérer le contenu textuel du lien
                const textContent = getTextContent(node);

                // Vérifier si c'est une citation (commence par @)
                if (textContent && /^@\w+/.test(textContent.trim())) {
                    // Trouver l'index du nœud dans son parent
                    const index = parent.children.indexOf(node);

                    if (index !== -1) {
                        // Remplacer le nœud link par un nœud text simple
                        parent.children[index] = {
                            type: 'text',
                            value: textContent.trim()
                        };
                    }
                }
            }
        };

        visit(tree, null);
    };
}

