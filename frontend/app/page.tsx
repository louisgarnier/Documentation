'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Header } from '@/src/components/Header';
import { ProjectItem } from '@/src/components/ProjectItem';
import { projectsAPI, exportAPI } from '@/src/api/client';
import type { Project } from '@/src/types';

export default function HomePage() {
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedProjectIds, setSelectedProjectIds] = useState<Set<number>>(new Set());
  const [exporting, setExporting] = useState(false);

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
    router.push('/project/new');
  };

  const handleSelectProject = (projectId: number) => {
    setSelectedProjectIds(prevIds => {
      const newIds = new Set(prevIds);
      if (newIds.has(projectId)) {
        newIds.delete(projectId);
      } else {
        newIds.add(projectId);
      }
      return newIds;
    });
  };

  const handleExportProjects = async () => {
    if (selectedProjectIds.size === 0) {
      setError('Please select at least one project to export.');
      return;
    }

    try {
      setExporting(true);
      setError(null);
      
      const blob = await exportAPI.exportToExcel({
        project_ids: Array.from(selectedProjectIds)
      });
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `projects_export_${new Date().toISOString().split('T')[0]}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Error exporting projects:', err);
      setError(err instanceof Error ? err.message : 'Failed to export projects');
    } finally {
      setExporting(false);
    }
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
            {selectedProjectIds.size > 0 && (
              <p className="text-sm text-blue-600 dark:text-blue-400 mt-1">
                {selectedProjectIds.size} {selectedProjectIds.size === 1 ? 'project' : 'projects'} selected
              </p>
            )}
          </div>
          <div className="flex items-center gap-3">
            {selectedProjectIds.size > 0 && (
              <button
                onClick={handleExportProjects}
                disabled={exporting}
                className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {exporting ? 'Exporting...' : `📥 Export (${selectedProjectIds.size})`}
              </button>
            )}
            <button
              onClick={handleCreateProject}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold transition-colors"
            >
              ➕ Create New Project
            </button>
          </div>
        </div>

        {loading && (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Loading projects...</p>
          </div>
        )}

        {error && (
          <div className={`rounded-lg p-4 mb-6 ${
            error.includes('Please select') 
              ? 'bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800'
              : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
          }`}>
            <p className={error.includes('Please select') 
              ? 'text-yellow-800 dark:text-yellow-200' 
              : 'text-red-800 dark:text-red-200'
            }>
              {error.includes('Please select') ? error : `Error: ${error}`}
            </p>
            {!error.includes('Please select') && (
              <button
                onClick={loadProjects}
                className="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline"
              >
                Try again
              </button>
            )}
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
              <ProjectItem 
                key={project.id} 
                project={project}
                selected={selectedProjectIds.has(project.id)}
                onSelect={handleSelectProject}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

