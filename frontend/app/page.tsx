'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Header } from '@/src/components/Header';
import { ProjectItem } from '@/src/components/ProjectItem';
import { projectsAPI } from '@/src/api/client';
import type { Project } from '@/src/types';

export default function HomePage() {
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProjects();
  }, []);

  // Reload projects when returning to this page (e.g., after creating a project)
  useEffect(() => {
    const handleFocus = () => {
      loadProjects();
    };
    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await projectsAPI.getAll();
      setProjects(data);
    } catch (err) {
      console.error('Error loading projects:', err);
      setError(err instanceof Error ? err.message : 'Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = () => {
    // TODO: Navigate to create project page or open modal
    // For now, we'll navigate to a create page
    router.push('/project/new');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
              Projects
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Manage your test case projects
            </p>
          </div>
          <button
            onClick={handleCreateProject}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold transition-colors"
          >
            ➕ Create New Project
          </button>
        </div>

        {loading && (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Loading projects...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
            <p className="text-red-800 dark:text-red-200">Error: {error}</p>
            <button
              onClick={loadProjects}
              className="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline"
            >
              Try again
            </button>
          </div>
        )}

        {!loading && !error && projects.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
              No projects yet. Create your first project to get started!
            </p>
            <button
              onClick={handleCreateProject}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold transition-colors"
            >
              ➕ Create New Project
            </button>
          </div>
        )}

        {!loading && !error && projects.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <ProjectItem key={project.id} project={project} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

