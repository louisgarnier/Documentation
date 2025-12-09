'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Header } from '@/src/components/Header';
import { ProjectForm } from '@/src/components/ProjectForm';
import { projectsAPI } from '@/src/api/client';

export default function NewProjectPage() {
  const router = useRouter();

  const handleSave = async (data: { name: string; description?: string | null }) => {
    const project = await projectsAPI.create(data);
    router.push(`/project/${project.id}`);
  };

  const handleCancel = () => {
    router.push('/');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-grow max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <Link 
          href="/"
          className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mb-6"
        >
          ← Back to Projects
        </Link>
        <ProjectForm onSave={handleSave} onCancel={handleCancel} />
      </main>
    </div>
  );
}

