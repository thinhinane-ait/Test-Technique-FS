'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Separator } from '@/components/ui/separator';
import { AlertTriangle, MessageSquare, Search, Loader2 } from 'lucide-react';
import { error } from 'console';
import { toast } from 'sonner';

type Incident = {
  id: number;
  title: string;
  description?: string;
  status: string;
  siteCode: string;
  createdAt: string;
  assignedTo: string | null;
  commentCount?: number;
  latitude?: string;
  longitude?: string;
};

type Comment = {
  id: number;
  author: string;
  message: string;
  createdAt: string;
};

async function fetchIncidents(status?: string, siteCode?: string, page = 1) {
  const params = new URLSearchParams({ page: String(page), limit: '10' });
  if (status && status !== 'all') params.set('status', status);
  if (siteCode) params.set('siteCode', siteCode);

  const res = await fetch(`/api/incidents?${params}`, {
    cache: 'no-store'
  });

  return res.json();
}


async function fetchIncidentDetail(id: number) {
  const res = await fetch(`/api/incidents/${id}`);
  return res.json();
}

async function updateIncidentStatus(id: number, status: string) {
  const res = await fetch(`/api/incidents/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
  return res.json();
}

async function fetchComments(id: number, page=1, limit=10) {
  const res = await fetch(`/api/incidents/${id}/comments?page=${page}&limit=${limit}`);
  console.log("res :",res);
  return res.json();
}

async function postComment(id: number, author: string, message: string) {
  const res = await fetch(`/api/incidents/${id}/comments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ author, message }),
  });
  return res.json();
}

export default function IncidentsClient() {
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [newComment, setNewComment] = useState('');

  /**
 * Rafraîchissement automatique de la liste,  refetchInterval:10000,
 */
  const { data: listData, isLoading, isError } = useQuery({
    queryKey: ['incidents', statusFilter, searchQuery, page],
    queryFn: () => fetchIncidents(statusFilter, searchQuery, page),
    staleTime: 0,
  });

  const [comments, setComments] = useState<Comment[]>([]);
  const [commentsLoading, setCommentsLoading] = useState(false);

  useEffect(() => {
    if (selectedIncident) {
      setCommentsLoading(true);
      fetchComments(selectedIncident.id)
        .then((res: any) => {
          console.log("Commentaires reçus :", res.data);
          setComments(res.data || []);
          setCommentsLoading(false);
        })
        .catch(() => setCommentsLoading(false));
    }
  }, [selectedIncident?.id]);

  const statusMutation = useMutation({
    mutationFn: ({ id, status }: { id: number; status: string }) =>
      updateIncidentStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });

  const commentMutation = useMutation({
    mutationFn: ({ id, message }: { id: number; message: string }) =>
      postComment(id, 'candidate@company.com', message),
    onSuccess: () => {
      setNewComment('');
      console.log("Commentaire ajouté avec succés");
      toast.success("Commentaire ajouté avec succés")
      if (selectedIncident) {
        setCommentsLoading(true);
        fetchComments(selectedIncident.id).then((res: any) => {
          setComments(res.data || []);
          setCommentsLoading(false);
        });
      }
    },
    onError:(error:Error) => {
      console.log(error.message);
      
      toast.error(
        error.message || "Impossible d'ajouter le commentaire"
      )
    }
    
  });

  const handleOpenDetail = (incident: Incident) => {
    setSelectedIncident(incident);
    setModalOpen(true);
  };

  const handleStatusChange = async (incidentId: number, newStatus: string) => {
    statusMutation.mutate({ id: incidentId, status: newStatus });
  };

  const handleSendComment = () => {
    if (!newComment.trim() || !selectedIncident) return;
    commentMutation.mutate({ id: selectedIncident.id, message: newComment });
  };

  const incidents: Incident[] = listData?.data || [];
  const total = listData?.total || 0;

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Incidents</h1>

      <div className="flex gap-3 items-center">
        <Select value={statusFilter} onValueChange={(v) => { if (v) { setStatusFilter(v); setPage(1); } }}>
          <SelectTrigger className="w-44">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem value="open">Open</SelectItem>
            <SelectItem value="inProgress">In Progress</SelectItem>
            <SelectItem value="resolved">Resolved</SelectItem>
          </SelectContent>
        </Select>

        <div className="relative flex-1 max-w-xs">
          <Search className="absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
          <Input
            placeholder="Search site code..."
            value={searchQuery}
            onChange={(e) => { setSearchQuery(e.target.value); setPage(1); }}
            className="pl-9"
          />
        </div>
      </div>

      {isLoading && (
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <Skeleton key={i} className="h-16 w-full rounded-lg" />
          ))}
        </div>
      )}

      {isError && (
        <div className="flex items-center gap-2 text-red-600">
          <AlertTriangle className="size-4" />
          Failed to load incidents.
        </div>
      )}

      {!isLoading && !isError && (
        <div className="space-y-2">
          {incidents.length === 0 ? (
            <p className="text-muted-foreground text-center py-8">No incidents found.</p>
          ) : (
            incidents.map((incident) => (
              <div
                key={incident.id}
                onClick={() => handleOpenDetail(incident)}
                className="flex items-center justify-between p-4 rounded-lg border cursor-pointer hover:bg-muted/50 transition-colors"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{incident.title}</span>
                    <StatusBadge status={incident.status} />
                  </div>
                  <div className="flex items-center gap-3 text-sm text-muted-foreground">
                    <span>{incident.siteCode}</span>
                    <span>{new Date(incident.createdAt).toLocaleDateString()}</span>
                    {incident.assignedTo && <span>{incident.assignedTo}</span>}
                  </div>
                </div>
                <div className="flex items-center gap-1 text-muted-foreground">
                  <MessageSquare className="size-4" />
                  <span className="text-sm">{incident.commentCount ?? 0}</span>
                </div>
              </div>
            ))
          )}

          {total > 10 && (
            <div className="flex justify-center gap-2 pt-4">
              <Button
                variant="outline"
                size="sm"
                disabled={page === 1}
                onClick={() => setPage(p => p - 1)}
              >
                Previous
              </Button>
              <span className="flex items-center text-sm text-muted-foreground px-2">
                Page {page} / {Math.ceil(total / 10)}
              </span>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= Math.ceil(total / 10)}
                onClick={() => setPage(p => p + 1)}
              >
                Next
              </Button>
            </div>
          )}
        </div>
      )}

      <Dialog open={modalOpen} onOpenChange={setModalOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          {selectedIncident && (
            <>
              <DialogHeader>
                <div className="flex items-center gap-3">
                  <DialogTitle>{selectedIncident.title}</DialogTitle>
                  <StatusBadge status={selectedIncident.status} />
                </div>
              </DialogHeader>

              <div className="space-y-4">
                {/* Info */}
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <span className="text-muted-foreground">Site:</span>{' '}
                    {selectedIncident.siteCode}
                  </div>
                  <div>
                    <span className="text-muted-foreground">Created:</span>{' '}
                    {new Date(selectedIncident.createdAt).toLocaleString()}
                  </div>
                  <div>
                    <span className="text-muted-foreground">Assigned:</span>{' '}
                    {selectedIncident.assignedTo || 'Unassigned'}
                  </div>
                  <div>
                    <span className="text-muted-foreground">Status:</span>{' '}
                    <Select
                      value={selectedIncident.status}
                      onValueChange={(v) => { if (v) handleStatusChange(selectedIncident.id, v); }}
                    >
                      <SelectTrigger className="w-36 h-8 inline-flex">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="open">Open</SelectItem>
                        <SelectItem value="inProgress">In Progress</SelectItem>
                        <SelectItem value="resolved">Resolved</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {selectedIncident.description && (
                  <div>
                    <h3 className="font-medium mb-1">Description</h3>
                    <p className="text-sm text-muted-foreground">
                      {selectedIncident.description}
                    </p>
                  </div>
                )}

                <Separator />

                <div>
                  <h3 className="font-medium mb-3">
                    Comments ({comments.length})
                  </h3>

                  {commentsLoading ? (
                    <div className="space-y-2">
                      <Skeleton className="h-10 w-full" />
                      <Skeleton className="h-10 w-3/4" />
                    </div>
                  ) : comments.length === 0 ? (
                    <p className="text-sm text-muted-foreground">No comments yet.</p>
                  ) : (
                    <div className="space-y-3 mb-4">
                      {comments.map((comment) => (
                        <div key={comment.id} className="rounded-md border p-3 space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-medium">{comment.author}</span>
                            <span className="text-xs text-muted-foreground">
                              {new Date(comment.createdAt).toLocaleString()}
                            </span>
                          </div>
                          <p className="text-sm">{comment.message}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="space-y-2 pt-2">
                    <Textarea
                      placeholder="Write a comment..."
                      value={newComment}
                      onChange={(e) => setNewComment(e.target.value)}
                      rows={2}
                    />
                    <div className="flex justify-end">
                      <Button
                        size="sm"
                        onClick={handleSendComment}
                        disabled={!newComment.trim() || commentMutation.isPending}
                      >
                        {commentMutation.isPending && <Loader2 className="size-3 mr-1.5 animate-spin" />}
                        Send
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors: any = {
    open: 'bg-red-100 text-red-700',
    inProgress: 'bg-blue-100 text-blue-700',
    resolved: 'bg-green-100 text-green-700',
  };

  return (
    <Badge variant="secondary" className={colors[status] || 'bg-gray-100 text-gray-700'}>
      {status.replace(/([A-Z])/g, ' $1').toLowerCase().trim()}
    </Badge>
  );
}
