'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { Header } from '@/src/components/Header';
import { TestCaseList } from '@/src/components/TestCaseList';
import { ProjectForm } from '@/src/components/ProjectForm';
import { projectsAPI, testCasesAPI } from '@/src/api/client';
import type { Project, TestCase } from '@/src/types';

export default function ProjectDetailPage() {
  const router = useRouter();
  const params = useParams();
  const projectId = parseInt(params.id as string);

  const [project, setProject] = useState<Project | null>(null);
  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [selectedTestCaseIds, setSelectedTestCaseIds] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingProject, setEditingProject] = useState(false);
  const [allProjects, setAllProjects] = useState<Project[]>([]);

  useEffect(() => {
    if (projectId) {
      loadProject();
      loadTestCases();
      loadAllProjects();
    }
  }, [projectId]);

  // Refresh projects list periodically to catch deletions
  useEffect(() => {
    if (!projectId) return;
    
    const interval = setInterval(() => {
      loadAllProjects();
    }, 5000); // Refresh every 5 seconds
    
    return () => clearInterval(interval);
  }, [projectId]);

  const loadProject = async () => {
    try {
      const data = await projectsAPI.getById(projectId);
      setProject(data);
    } catch (err) {
      console.error('Error loading project:', err);
      setError(err instanceof Error ? err.message : 'Failed to load project');
    }
  };

  const loadTestCases = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await testCasesAPI.getAll(projectId);
      setTestCases(data);
    } catch (err) {
      console.error('Error loading test cases:', err);
      setError(err instanceof Error ? err.message : 'Failed to load test cases');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTestCase = (id: number) => {
    setSelectedTestCaseIds(prevIds => {
      const newIds = new Set(prevIds);
      if (newIds.has(id)) {
        newIds.delete(id);
      } else {
        newIds.add(id);
      }
      return newIds;
    });
  };

  const handleViewDetail = (testCase: TestCase) => {
    router.push(`/test-case/${testCase.id}`);
  };

  const loadAllProjects = async () => {
    try {
      const data = await projectsAPI.getAll();
      setAllProjects(data);
    } catch (err) {
      console.error('Error loading projects:', err);
    }
  };

  const handleSaveProject = async (data: { name: string; description?: string | null }) => {
    try {
      const updated = await projectsAPI.update(projectId, data);
      setProject(updated);
      setEditingProject(false);
      // Reload projects list to update counts
      await loadAllProjects();
    } catch (err) {
      throw err;
    }
  };

  const handleDeleteProject = async () => {
    try {
      await projectsAPI.delete(projectId);
      // Navigate away after delete
      router.push('/');
    } catch (err) {
      throw err;
    }
  };

  const handleDuplicateTestCase = async (testCaseId: number, targetProjectId?: number) => {
    try {
      const testCase = testCases.find(tc => tc.id === testCaseId);
      if (!testCase) return;

      // Generate unique test number with timestamp to avoid conflicts
      const timestamp = Date.now();
      const newTestNumber = `${testCase.test_number}_COPY_${timestamp}`;
      
      await testCasesAPI.duplicate(testCaseId, {
        new_test_number: newTestNumber,
        target_project_id: targetProjectId
      });
      
      // Reload test cases
      await loadTestCases();
      // Reload project to update count
      await loadProject();
    } catch (err) {
      console.error('Error duplicating test case:', err);
      alert(err instanceof Error ? err.message : 'Failed to duplicate test case');
    }
  };

  const handleMoveTestCase = async (testCaseId: number, targetProjectId: number | null) => {
    try {
      // Validate target project exists if provided
      if (targetProjectId !== null) {
        const targetProject = allProjects.find(p => p.id === targetProjectId);
        if (!targetProject) {
          alert(`Error: Target project (ID: ${targetProjectId}) no longer exists. Please refresh the page and try again.`);
          // Refresh projects list
          await loadAllProjects();
          return;
        }
      }

      await testCasesAPI.move(testCaseId, {
        target_project_id: targetProjectId
      });
      
      // Reload test cases
      await loadTestCases();
      // Reload project to update count
      await loadProject();
      // Reload all projects to get fresh list (in case any were deleted)
      await loadAllProjects();
    } catch (err) {
      console.error('Error moving test case:', err);
      alert(err instanceof Error ? err.message : 'Failed to move test case');
      // Refresh projects list on error
      await loadAllProjects();
    }
  };

  const handleCreateTestCase = () => {
    router.push(`/test-case/new?project_id=${projectId}`);
  };

  if (loading && !project) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
        <Header />
        <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Loading project...</p>
          </div>
        </main>
      </div>
    );
  }

  if (error && !project) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
        <Header />
        <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-800 dark:text-red-200">Error: {error}</p>
            <Link href="/" className="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline">
              ← Back to Projects
            </Link>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {/* Back to Projects Link */}
        <Link 
          href="/"
          className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mb-6"
        >
          ← Back to Projects
        </Link>

        {/* Project Header */}
        {project && !editingProject && (
          <div className="mb-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                  {project.name}
                </h1>
                {project.description && (
                  <p className="text-gray-600 dark:text-gray-400 text-lg mb-2">
                    {project.description}
                  </p>
                )}
                <p className="text-sm text-gray-500 dark:text-gray-500">
                  {testCases.length} {testCases.length === 1 ? 'test case' : 'test cases'}
                </p>
              </div>
              <div className="flex items-center gap-3 ml-4">
                <button
                  onClick={() => setEditingProject(true)}
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 font-semibold transition-colors"
                >
                  ✏️ Edit Project
                </button>
                <button
                  onClick={handleCreateTestCase}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold transition-colors"
                >
                  ➕ Create Test Case
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Edit Project Form */}
        {project && editingProject && (
          <div className="mb-6">
            <ProjectForm
              project={project}
              onSave={handleSaveProject}
              onCancel={() => setEditingProject(false)}
              onDelete={handleDeleteProject}
            />
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
            <p className="text-red-800 dark:text-red-200">Error: {error}</p>
            <button
              onClick={loadTestCases}
              className="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline"
            >
              Try again
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Loading test cases...</p>
          </div>
        )}

        {/* Test Cases List */}
        {!loading && !error && !editingProject && (
          <TestCaseList
            testCases={testCases}
            selectedTestCaseIds={selectedTestCaseIds}
            onSelectTestCase={handleSelectTestCase}
            onViewDetail={handleViewDetail}
            onDuplicate={handleDuplicateTestCase}
            onMove={handleMoveTestCase}
            currentProjectId={projectId}
            allProjects={allProjects}
            onRefreshProjects={loadAllProjects}
          />
        )}
      </main>
    </div>
  );
}

