##  Installation 

Aprés avoir récupérer le projet frontend j'ai installé les dépendances avec 

```bash
 npm install
```

J'ai crée le fichier `.env.local` à la racine afin de définir l'adresse backend `API_BASE_URL` :

```
API_BASE_URL=http://localhost:4000
```

J'ai lancé l'application

```bash
npm run dev
```
L'application est ensuite accessible à l'adresse :

```
http://localhost:3000/incidents
```
## A FAIRE — Nouvelles fonctionnalités
### 1. Rafraîchissement automatique de la liste

- La liste doit se rafraîchir automatiquement toutes les **10 secondes**
- Le rafraîchissement doit être **silencieux** (pas de spinner / flash blanc à chaque poll)
- Les actions utilisateur (filtre, pagination) doivent afficher un loading normal

#### La liste doit se rafraîchir automatiquement toutes les **10 secondes** : 

Dans le fichier src/app/incidents/incidents-clients.tsx, j'ai utilisé **TanStack Query** en ajoutant les options `refetchInterval` et `staleTime` dans `useQuery`

 - `refetchInterval`: 10000:  permet de rafraîchir automatiquement la liste toutes les 10 secondes.
    `staleTime`:0 : garantit que les données sont considérées comme immédiatement périmées afin que chaque rafraîchissement récupère les informations les plus récentes.

 ```tsx
  const { data: listData, isLoading, isError } = useQuery({
    queryKey: ['incidents', statusFilter, searchQuery, page],
    queryFn: () => fetchIncidents(statusFilter, searchQuery, page),
    refetchInterval: 10000,
    staleTime: 0,
  });
```
#### Le rafraîchissement doit être **silencieux** (pas de spinner / flash blanc à chaque poll) : 

Pour cette partie, je n'ai pas eu de modification à apporter, car ce comportement était déjà présent dans le projet.

Le composant utilise l'état `isLoading` de TanStack Query pour afficher le `Skeleton` uniquement lors du chargement initial de la liste. Une fois les données chargées, `isLoading` passe à `false` et n'est pas réactivé lors des rafraîchissements automatiques.


#### Les actions utilisateur (filtre, pagination) doivent afficher un loading normal: 
 Pour cela j'ai ajouté un état `userActionLoading` afin de distinguer les actions déclenchées par l'utilisateur du rafraîchissement automatique de la liste.
 ```tsx
    const [userActionLoading, setUserActionLoading] = useState(false);
  ```
 Lorsque l'utilisateur effectue une recherche ou change le filtre, `userActionLoading` est activé et le composant `Skeleton` est affiché pendant le chargement des nouvelles données. 

 À la fin de la requête, TanStack Query met isFetching à false, ce qui permet de désactiver `userActionLoading` et d'afficher la nouvelle liste.

 ```tsx
    useEffect(() => {
    if (!isFetching) {
      setUserActionLoading(false);
    }
  }, [isFetching]);
  ```
### 2. Amélioration de la section commentaires

- Pagination des commentaires (le backend supporte `?page=&limit=`)
- Ajout d'un commentaire avec confirmation utilisateur (toast de confirmation / erreur)
- Mettre en place un test unitaire (s'il vous reste du temps)


#### Pagination des commentaires (le backend supporte `?page=&limit=`) : 
Comme l'API côté backend prend déjà en charge les paramètres `page` et `limit`, j'ai adapté la fonction `fetchComments` afin d'utiliser cette pagination.

 ```tsx
async function fetchComments(id: number, page=1, limit=10) {
  const res = await fetch(`/api/incidents/${id}/comments?page=${page}&limit=${limit}`);
  return res.json();
}
  ```


#### Ajout d'un commentaire avec confirmation utilisateur (toast de confirmation / erreur) : 
Pour cette partie, j'ai utilisé la bibliothèque **Sonner** afin d'informer l'utilisateur du résultat de l'ajout d'un commentaire.

Dans le `useMutation`, j'ai ajouté :
- `toast.success()` dans `onSuccess` pour afficher un message lorsque le commentaire est ajouté avec succès ;
- `toast.error()` dans `onError` pour afficher un message en cas d'échec.

J'ai également ajouté le composant `Toaster` dans la page principale (`page.tsx`) afin que les notifications puissent être affichées dans l'application.

 ```tsx
  const commentMutation = useMutation({
    mutationFn: ({ id, message }: { id: number; message: string }) =>
      postComment(id, 'candidate@company.com', message),
    onSuccess: () => {
      setNewComment('');
      toast.success("Commentaire ajouté avec succès")
      setCommentPage(commentTotalPages);
      if (selectedIncident) {
        setCommentsLoading(true);
        fetchComments(selectedIncident.id,commentPage,commentLimit).then((res: any) => {
          setComments(res.data || []);
          setCommentsLoading(false);
        });
      }
    },
    onError:(error:Error) => {
      toast.error(
        error.message || "Impossible d'ajouter le commentaire"
      )
    }
    
  });

 ```

#### Mettre en place un test unitaire (s'il vous reste du temps):
Pour cette partie j'ai installé **Vitest** comme framework de test.
J'ai ensuite ajouté les scripts suivants dans le `package.json` :
```json
"scripts": {
  "test": "vitest",
  "test:run": "vitest run"
}
```
J'ai créé un dossier `src/services` contenant un fichier `comments.ts`, dans lequel j'ai placé la fonction `postComment`, afin de pouvoir la tester indépendamment du composant React.

J'ai ensuite créé le fichier `comments.test.ts` qui contient un test unitaire vérifiant le bon fonctionnement de `postComment`.
Enfin, j'ai exécuté les tests avec la commande :

```bash
npm run test:run
```
Le test vérifie que la fonction envoie correctement une requête HTTP `POST` vers l'API avec les paramètres attendus et qu'elle retourne la réponse de l'API.