<svelte:options runes={false} />

<script>
  import '../../../styles/admin-dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import { API_BASE, apiFetch, getStoredToken } from '$lib/api/api.js';
  import {
    deleteJob,
    deleteUser,
    getAdminAnalytics,
    getAdminJobs,
    getAdminOverview,
    getAdminUser,
    getAdminUsers,
    getSystemHealth,
    updateUserStatus
  } from '$lib/api/adminApi.js';
  import AdminLayout from '$lib/components/admin/AdminLayout.svelte';
  import AdminSidebar from '$lib/components/admin/AdminSidebar.svelte';
  import AdminTopbar from '$lib/components/admin/AdminTopbar.svelte';
  import AdminStatsCards from '$lib/components/admin/AdminStatsCards.svelte';
  import AdminCharts from '$lib/components/admin/AdminCharts.svelte';
  import AdminUsersTable from '$lib/components/admin/AdminUsersTable.svelte';
  import AdminJobsTable from '$lib/components/admin/AdminJobsTable.svelte';
  import AdminSystemHealth from '$lib/components/admin/AdminSystemHealth.svelte';
  import AdminConfirmModal from '$lib/components/admin/AdminConfirmModal.svelte';
  import AdminToast from '$lib/components/admin/AdminToast.svelte';
  import AdminStatusBadge from '$lib/components/admin/AdminStatusBadge.svelte';

  const PAGE_SIZE = 10;
  const AUTH_STORAGE_KEYS = ['token', 'token_type', 'role', 'user_name', 'authToken', 'access_token', 'refresh_token'];
  const sections = [
    { id: 'overview', label: 'Overview', icon: 'O' },
    { id: 'users', label: 'Users', icon: 'U' },
    { id: 'jobs', label: 'Processing Jobs', icon: 'J' },
    { id: 'health', label: 'System Health', icon: 'H' }
  ];

  let activeSection = 'overview';
  let sidebarCollapsed = false;
  let mobileSidebarOpen = false;
  let accessDenied = false;
  let bootLoading = true;
  let globalLoading = false;
  let overviewLoading = true;
  let usersLoading = true;
  let jobsLoading = true;
  let healthLoading = true;
  let toast = null;
  let toastTimer;
  let refreshTimer;
  let search = '';
  let debouncedSearch = '';
  let usersStatus = '';
  let jobsStatus = '';
  let usersPage = 1;
  let jobsPage = 1;
  let admin = { name: 'Admin', email: '' };
  let currentAdminId = null;

  let overview = null;
  let analytics = { weekly_processing: [], status_distribution: {}, share_activity: [], user_growth: [] };
  let users = [];
  let usersTotal = 0;
  let jobs = [];
  let jobsTotal = 0;
  let health = null;
  let topError = '';

  let detailModal = { open: false, title: '', type: '', item: null };
  let confirmState = { open: false, title: '', message: '', confirmLabel: 'Confirm', tone: 'danger', busy: false, action: null };

  function showToast(type, message, title = 'Notice') {
    toast = { type, message, title };
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast = null;
    }, 3200);
  }

  function formatDate(value) {
    if (!value) return '--';
    return new Intl.DateTimeFormat('en-IN', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value));
  }

  function formatDuration(value) {
    if (value === null || value === undefined || value === '') return '--';
    return `${Number(value).toFixed(2)} sec`;
  }

  function pageCount(total) {
    return Math.max(1, Math.ceil((total || 0) / PAGE_SIZE));
  }

  function normalizeAdminAssetUrl(url) {
    if (!url || typeof url !== 'string') return null;

    const trimmed = url.trim();
    if (!trimmed) return null;
    if (/^(https?:|data:|blob:)/i.test(trimmed)) return trimmed;
    if (/^\/\//.test(trimmed)) return `https:${trimmed}`;
    if (/^(file:|[a-zA-Z]:[\\/])/.test(trimmed)) return null;

    const normalizedPath = trimmed.startsWith('/') ? trimmed : `/${trimmed.replace(/^\.?\//, '')}`;
    return `${API_BASE}${normalizedPath}`;
  }

  function mapStats() {
    const stats = overview?.stats || {};
    return [
      { label: 'Total Users', value: stats.total_users ?? 0, helper: 'Registered platform accounts', icon: 'U', tone: 'primary' },
      { label: 'Images Processed', value: stats.total_images_processed ?? 0, helper: 'Completed output images', icon: 'I', tone: 'info' },
      { label: 'Successful Jobs', value: stats.successful_jobs ?? 0, helper: 'Completed without failure', icon: 'S', tone: 'success' },
      { label: 'Failed Jobs', value: stats.failed_jobs ?? 0, helper: 'Need admin review', icon: 'F', tone: 'danger' },
      { label: 'Active Batch Jobs', value: stats.active_batch_jobs ?? 0, helper: 'Queued or processing batches', icon: 'B', tone: 'warning' }
    ];
  }

  function mapHealthCards() {
    if (!health) return [];
    return [
      { label: 'API Status', status: health.api_status, value: 'Admin API reachable' },
      { label: 'Database Status', status: health.database_status, value: 'PostgreSQL connection state' },
      { label: 'ML Model Status', status: health.ml_model_status, value: 'Reported without reload' },
      { label: 'Storage Used', value: `${health.storage_used_mb ?? 0} MB` },
      { label: 'Avg Processing Time', value: `${health.avg_processing_time_sec ?? 0} sec` },
      { label: 'Failed Jobs', value: String(health.failed_jobs_count ?? 0) }
    ];
  }

  function openConfirm(config) {
    confirmState = { ...confirmState, open: true, busy: false, ...config };
  }

  function closeConfirm() {
    confirmState = { ...confirmState, open: false, busy: false, action: null };
  }

  async function runConfirm() {
    if (!confirmState.action) return;
    confirmState = { ...confirmState, busy: true };
    try {
      await confirmState.action();
    } finally {
      closeConfirm();
    }
  }

  function closeDetail() {
    detailModal = { open: false, title: '', type: '', item: null };
  }

  async function loadAdminProfile() {
    const response = await apiFetch('/api/v1/users/me');
    const payload = await response.json().catch(() => null);

    if (response.status === 401) {
      goto('/login');
      return false;
    }

    if (!response.ok) {
      throw new Error(payload?.detail || 'Unable to load admin profile');
    }

    currentAdminId = payload.id;
    admin = { name: payload.name || 'Admin', email: payload.email || '' };
    localStorage.setItem('user_name', admin.name);

    if (payload.role !== 'admin' && localStorage.getItem('role') !== 'admin') {
      accessDenied = true;
      return false;
    }

    localStorage.setItem('role', payload.role || 'user');
    return true;
  }

  async function guardAdminError(error) {
    if (error?.status === 401) {
      goto('/login');
      return true;
    }
    if (error?.status === 403) {
      accessDenied = true;
      topError = 'Admin access required.';
      return true;
    }
    return false;
  }

  async function loadOverviewData() {
    overviewLoading = true;
    try {
      const [overviewData, analyticsData, healthData] = await Promise.all([
        getAdminOverview(),
        getAdminAnalytics(),
        getSystemHealth()
      ]);
      overview = overviewData;
      analytics = analyticsData;
      health = healthData;
    } catch (error) {
      if (!(await guardAdminError(error))) {
        topError = error.message || 'Failed to load overview.';
      }
    } finally {
      overviewLoading = false;
      healthLoading = false;
    }
  }

  async function loadUsersData() {
    usersLoading = true;
    try {
      const data = await getAdminUsers({
        search: debouncedSearch,
        status: usersStatus || undefined,
        limit: PAGE_SIZE,
        offset: (usersPage - 1) * PAGE_SIZE
      });
      users = (data.items || []).map((item) => ({
        ...item,
        joinedAt: formatDate(item.joined_at),
        totalUploads: item.total_uploads
      }));
      usersTotal = data.total || 0;
    } catch (error) {
      if (!(await guardAdminError(error))) {
        topError = error.message || 'Failed to load users.';
      }
    } finally {
      usersLoading = false;
    }
  }

  async function loadJobsData() {
    jobsLoading = true;
    try {
      const data = await getAdminJobs({
        search: debouncedSearch,
        status: jobsStatus || undefined,
        limit: PAGE_SIZE,
        offset: (jobsPage - 1) * PAGE_SIZE
      });
      jobs = (data.items || []).map((item) => {
        const originalUrl = normalizeAdminAssetUrl(item.original_url);
        const processedUrl = normalizeAdminAssetUrl(item.processed_url);
        const imageUrl = normalizeAdminAssetUrl(item.image_url);
        const fileUrl = normalizeAdminAssetUrl(item.file_url);

        return {
          ...item,
          userName: item.user_name || 'Guest',
          thumbnailUrl:
            normalizeAdminAssetUrl(item.thumbnail_url) ||
            originalUrl ||
            processedUrl ||
            imageUrl ||
            fileUrl,
          originalUrl,
          processedUrl,
          imageUrl,
          fileUrl,
          createdAt: formatDate(item.created_at),
          processingTimeLabel: formatDuration(item.processing_time)
        };
      });
      jobsTotal = data.total || 0;
    } catch (error) {
      if (!(await guardAdminError(error))) {
        topError = error.message || 'Failed to load jobs.';
      }
    } finally {
      jobsLoading = false;
    }
  }

  async function refreshCurrentSection() {
    globalLoading = true;
    topError = '';
    try {
      if (activeSection === 'overview') {
        await loadOverviewData();
        await Promise.all([loadUsersData(), loadJobsData()]);
      } else if (activeSection === 'users') {
        await loadUsersData();
      } else if (activeSection === 'jobs') {
        await loadJobsData();
      } else if (activeSection === 'health') {
        healthLoading = true;
        health = await getSystemHealth();
        healthLoading = false;
      }
    } catch (error) {
      if (!(await guardAdminError(error))) {
        topError = error.message || 'Failed to refresh dashboard.';
      }
    } finally {
      globalLoading = false;
      bootLoading = false;
    }
  }

  async function openUserDetail(user) {
    try {
      const detail = await getAdminUser(user.id);
      detailModal = {
        open: true,
        type: 'user',
        title: user.name,
        item: {
          ...detail,
          joinedAt: formatDate(detail.joined_at),
          lastLogin: formatDate(detail.last_login),
          recentJobs: (detail.recent_jobs || []).map((job) => ({
            ...job,
            createdAt: formatDate(job.created_at),
            processingTimeLabel: formatDuration(job.processing_time)
          }))
        }
      };
    } catch (error) {
      if (!(await guardAdminError(error))) {
        showToast('error', error.message || 'Unable to load user details.', 'Error');
      }
    }
  }

  function openJobDetail(job) {
    detailModal = { open: true, type: 'job', title: job.filename, item: job };
  }

  function handleLogout() {
    AUTH_STORAGE_KEYS.forEach((key) => {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
    });
    showToast('success', 'Logged out successfully.', 'Success');
    setTimeout(() => goto('/login'), 250);
  }

  function handleSearch(value) {
    search = value;
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(async () => {
      debouncedSearch = value.trim();
      usersPage = 1;
      jobsPage = 1;
      await refreshCurrentSection();
    }, 300);
  }

  async function handleUserToggle(user) {
    if (user.id === currentAdminId) {
      showToast('error', 'You cannot disable your own account.', 'Action blocked');
      return;
    }

    const nextStatus = user.status === 'active' ? 'disabled' : 'active';
    openConfirm({
      title: `${nextStatus === 'disabled' ? 'Disable' : 'Enable'} user`,
      message: `${nextStatus === 'disabled' ? 'Disable' : 'Enable'} ${user.name}?`,
      confirmLabel: nextStatus === 'disabled' ? 'Disable user' : 'Enable user',
      tone: nextStatus === 'disabled' ? 'danger' : 'primary',
      action: async () => {
        await updateUserStatus(user.id, nextStatus);
        showToast('success', `User ${nextStatus} successfully.`, 'Updated');
        await loadUsersData();
      }
    });
  }

  async function handleUserDelete(user) {
    if (user.id === currentAdminId) {
      showToast('error', 'You cannot delete your own account.', 'Action blocked');
      return;
    }

    openConfirm({
      title: 'Delete user',
      message: `Delete ${user.name} from the admin users list? Their account will be soft-deleted and hidden from active admin queries.`,
      confirmLabel: 'Delete user',
      tone: 'danger',
      action: async () => {
        await deleteUser(user.id);
        users = users.filter((item) => item.id !== user.id);
        usersTotal = Math.max(0, usersTotal - 1);
        showToast('success', 'User deleted successfully.', 'Updated');
        closeDetail();
        await loadUsersData();
      }
    });
  }

  function handleJobDelete(job) {
    openConfirm({
      title: 'Delete job',
      message: `Delete ${job.filename}? This removes the job record and linked files under uploads.`,
      confirmLabel: 'Delete job',
      tone: 'danger',
      action: async () => {
        await deleteJob(job.id);
        showToast('success', 'Job deleted successfully.', 'Updated');
        closeDetail();
        await loadJobsData();
        await loadOverviewData();
      }
    });
  }

  onMount(() => {
    if (!getStoredToken()) {
      goto('/login');
      return;
    }

    const handleResize = () => {
      sidebarCollapsed = window.innerWidth < 1180;
      if (window.innerWidth >= 900) {
        mobileSidebarOpen = false;
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    (async () => {
      try {
        const allowed = await loadAdminProfile();
        if (allowed) {
          await refreshCurrentSection();
        } else {
          bootLoading = false;
        }
      } catch (error) {
        if (!(await guardAdminError(error))) {
          topError = error.message || 'Admin dashboard failed to load.';
          bootLoading = false;
        }
      }
    })();

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });

  onDestroy(() => {
    clearTimeout(toastTimer);
    clearTimeout(refreshTimer);
  });
</script>

<svelte:head>
  <title>GlassClear Admin Dashboard</title>
</svelte:head>

<AdminToast {toast} onClose={() => (toast = null)} />

{#if accessDenied}
  <div class="gc-admin-main">
    <div class="gc-admin-error">Admin access required.</div>
  </div>
{:else}
  <AdminLayout detailOpen={detailModal.open}>
    <svelte:fragment slot="sidebar">
      <AdminSidebar
        items={sections}
        active={activeSection}
        collapsed={sidebarCollapsed}
        mobileOpen={mobileSidebarOpen}
        onToggle={() => (sidebarCollapsed = !sidebarCollapsed)}
        onCloseMobile={() => (mobileSidebarOpen = false)}
        onSelect={async (section) => {
          activeSection = section;
          mobileSidebarOpen = false;
          await refreshCurrentSection();
        }}
      />
    </svelte:fragment>

    <svelte:fragment slot="topbar">
      <AdminTopbar
        title={sections.find((section) => section.id === activeSection)?.label || 'Overview'}
        {search}
        {admin}
        onSearch={handleSearch}
        onRefresh={refreshCurrentSection}
        onLogout={handleLogout}
        onOpenMobile={() => (mobileSidebarOpen = true)}
      />
    </svelte:fragment>

    {#if topError}
      <div class="gc-admin-error">{topError}</div>
    {/if}

    {#if bootLoading}
      <div class="gc-admin-table-skeleton"></div>
      <div class="gc-admin-table-skeleton"></div>
    {:else if activeSection === 'overview'}
      <AdminStatsCards items={mapStats()} />
      <AdminCharts weeklyProcessing={analytics.weekly_processing} statusDistribution={analytics.status_distribution} />
      <div class="gc-admin-overview-grid">
        <AdminUsersTable items={users.slice(0, 5)} loading={usersLoading} onView={openUserDetail} onToggle={handleUserToggle} onDelete={handleUserDelete} />
        <AdminSystemHealth cards={mapHealthCards()} loading={healthLoading} />
      </div>
      <AdminJobsTable items={jobs.slice(0, 5)} loading={jobsLoading} onView={openJobDetail} onDelete={handleJobDelete} />
    {:else if activeSection === 'users'}
      <div class="gc-admin-panel">
        <div class="gc-admin-toolbar">
          <div>
            <span class="gc-admin-eyebrow">Filters</span>
            <h3>User controls</h3>
          </div>
          <div class="gc-admin-filter-row">
            <select bind:value={usersStatus} on:change={async () => { usersPage = 1; await loadUsersData(); }}>
              <option value="">All statuses</option>
              <option value="active">Active</option>
              <option value="disabled">Disabled</option>
            </select>
          </div>
        </div>
      </div>
      <AdminUsersTable items={users} loading={usersLoading} onView={openUserDetail} onToggle={handleUserToggle} onDelete={handleUserDelete} />
      <div class="gc-admin-panel">
        <div class="gc-admin-pagination">
          <button type="button" class="gc-admin-button gc-admin-button--ghost" disabled={usersPage === 1} on:click={async () => { usersPage -= 1; await loadUsersData(); }}>Previous</button>
          <span>Page {usersPage} of {pageCount(usersTotal)}</span>
          <button type="button" class="gc-admin-button gc-admin-button--ghost" disabled={usersPage >= pageCount(usersTotal)} on:click={async () => { usersPage += 1; await loadUsersData(); }}>Next</button>
        </div>
      </div>
    {:else if activeSection === 'jobs'}
      <div class="gc-admin-panel">
        <div class="gc-admin-toolbar">
          <div>
            <span class="gc-admin-eyebrow">Filters</span>
            <h3>Processing jobs</h3>
          </div>
          <div class="gc-admin-filter-row">
            <select bind:value={jobsStatus} on:change={async () => { jobsPage = 1; await loadJobsData(); }}>
              <option value="">All statuses</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
              <option value="processing">Processing</option>
              <option value="queued">Queued</option>
            </select>
          </div>
        </div>
      </div>
      <AdminJobsTable items={jobs} loading={jobsLoading} onView={openJobDetail} onDelete={handleJobDelete} />
      <div class="gc-admin-panel">
        <div class="gc-admin-pagination">
          <button type="button" class="gc-admin-button gc-admin-button--ghost" disabled={jobsPage === 1} on:click={async () => { jobsPage -= 1; await loadJobsData(); }}>Previous</button>
          <span>Page {jobsPage} of {pageCount(jobsTotal)}</span>
          <button type="button" class="gc-admin-button gc-admin-button--ghost" disabled={jobsPage >= pageCount(jobsTotal)} on:click={async () => { jobsPage += 1; await loadJobsData(); }}>Next</button>
        </div>
      </div>
    {:else if activeSection === 'health'}
      <AdminSystemHealth cards={mapHealthCards()} loading={healthLoading} />
      <AdminCharts weeklyProcessing={analytics.weekly_processing} statusDistribution={analytics.status_distribution} />
    {/if}
  </AdminLayout>
{/if}

{#if detailModal.open}
  <div class="gc-admin-modal-backdrop" role="presentation" on:click={closeDetail}>
    <div
      class="gc-admin-detail-modal"
      role="dialog"
      aria-modal="true"
      aria-label={detailModal.title}
      tabindex="-1"
      on:click|stopPropagation
      on:keydown|stopPropagation
    >
      <div class="gc-admin-modal__header">
        <div>
          <span class="gc-admin-eyebrow">Details</span>
          <h3>{detailModal.title}</h3>
        </div>
        <button type="button" class="gc-admin-icon-button" on:click={closeDetail} aria-label="Close details">x</button>
      </div>

      {#if detailModal.type === 'user'}
        <div class="gc-admin-detail-list">
          <div><span>Name</span><strong>{detailModal.item.name}</strong></div>
          <div><span>Email</span><strong>{detailModal.item.email}</strong></div>
          <div><span>Joined</span><strong>{detailModal.item.joinedAt}</strong></div>
          <div><span>Last Activity</span><strong>{detailModal.item.lastLogin}</strong></div>
          <div><span>Total Uploads</span><strong>{detailModal.item.total_uploads}</strong></div>
          <div><span>Status</span><AdminStatusBadge status={detailModal.item.status} /></div>
          <div>
            <span>Recent Jobs</span>
            <strong>{detailModal.item.recentJobs?.length ? detailModal.item.recentJobs.map((job) => job.filename).join(', ') : 'No recent jobs'}</strong>
          </div>
        </div>
      {:else if detailModal.type === 'job'}
        <div class="gc-admin-detail-list">
          <div><span>User</span><strong>{detailModal.item.userName}</strong></div>
          <div><span>Status</span><AdminStatusBadge status={detailModal.item.status} /></div>
          <div><span>Processing Time</span><strong>{detailModal.item.processingTimeLabel}</strong></div>
          <div><span>Created</span><strong>{detailModal.item.createdAt}</strong></div>
        </div>
        <div class="gc-admin-detail-modal__media">
          <img src={detailModal.item.originalUrl || detailModal.item.thumbnailUrl} alt={`${detailModal.item.filename} original`} />
          <img src={detailModal.item.processedUrl || detailModal.item.thumbnailUrl} alt={`${detailModal.item.filename} processed`} />
        </div>
      {/if}
    </div>
  </div>
{/if}

<AdminConfirmModal
  open={confirmState.open}
  title={confirmState.title}
  message={confirmState.message}
  confirmLabel={confirmState.confirmLabel}
  tone={confirmState.tone}
  busy={confirmState.busy}
  onConfirm={runConfirm}
  onClose={closeConfirm}
/>
