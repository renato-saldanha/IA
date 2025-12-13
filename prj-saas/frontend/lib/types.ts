export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'admin' | 'agent' | 'customer';
  is_active: boolean;
  organization_id: number | null;
  created_at: string;
}

export interface Ticket {
  id: number;
  subject: string;
  description: string;
  status: 'open' | 'in_progress' | 'waiting' | 'resolved' | 'closed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  channel: 'email' | 'chat' | 'form' | 'widget';
  organization_id: number;
  customer_id: number;
  assigned_to_id: number | null;
  created_at: string;
  updated_at: string;
  resolved_at: string | null;
  closed_at: string | null;
}

export interface TicketMessage {
  id: number;
  content: string;
  is_internal: boolean;
  ticket_id: number;
  author_id: number;
  created_at: string;
}

export interface KnowledgeArticle {
  id: number;
  title: string;
  slug: string;
  content: string;
  category: string;
  is_published: boolean;
  views_count: number;
  organization_id: number;
  author_id: number;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  organization_name?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

