import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { useState } from 'react';

import {
  ACTION_LABELS,
  NOTIFICATION_DURATION_MS,
  PAGE_TITLES,
} from '../../constants/messageConstants';
import { useEmployeeForm } from '../../controllers/useEmployeeForm';
import { useEmployees } from '../../controllers/useEmployees';
import type { Employee } from '../../models/employee';
import ConfirmDeleteDialog from '../components/ConfirmDeleteDialog';
import EmployeeFilters from '../components/EmployeeFilters';
import EmployeeFormDialog from '../components/EmployeeFormDialog';
import EmployeeTable from '../components/EmployeeTable';

export default function EmployeesPage() {
  const employees = useEmployees();
  const form = useEmployeeForm({ onSaved: employees.handleEmployeeSaved });
  const [employeeToDelete, setEmployeeToDelete] = useState<Employee | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const confirmDelete = async () => {
    if (!employeeToDelete) return;
    setIsDeleting(true);
    await employees.deleteEmployee(employeeToDelete.id);
    setIsDeleting(false);
    setEmployeeToDelete(null);
  };

  return (
    <>
      <Stack direction="row" sx={{ mb: 3, justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          {PAGE_TITLES.EMPLOYEES}
        </Typography>
        <Button variant="contained" onClick={form.openCreate}>
          {ACTION_LABELS.ADD}
        </Button>
      </Stack>

      <EmployeeFilters
        searchInput={employees.searchInput}
        filters={employees.params}
        filterOptions={employees.filterOptions}
        onSearchChange={employees.setSearch}
        onFilterChange={employees.setFilter}
        onClear={employees.clearFilters}
      />

      {employees.error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {employees.error}
        </Alert>
      )}

      <EmployeeTable
        employees={employees.employees}
        total={employees.total}
        page={employees.params.page}
        pageSize={employees.params.page_size}
        sortBy={employees.params.sort_by}
        sortOrder={employees.params.sort_order}
        isLoading={employees.isLoading}
        onPageChange={employees.setPage}
        onPageSizeChange={employees.setPageSize}
        onSort={employees.setSort}
        onEdit={form.openEdit}
        onDelete={setEmployeeToDelete}
      />

      <EmployeeFormDialog
        isOpen={form.isOpen}
        mode={form.mode}
        values={form.values}
        errors={form.errors}
        submitError={form.submitError}
        isSubmitting={form.isSubmitting}
        referenceData={form.referenceData}
        onChange={form.setField}
        onSubmit={form.submit}
        onClose={form.close}
      />

      <ConfirmDeleteDialog
        employee={employeeToDelete}
        isDeleting={isDeleting}
        onConfirm={confirmDelete}
        onCancel={() => setEmployeeToDelete(null)}
      />

      <Snackbar
        open={employees.notification !== null}
        autoHideDuration={NOTIFICATION_DURATION_MS}
        onClose={employees.dismissNotification}
        message={employees.notification}
      />
    </>
  );
}
