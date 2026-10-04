import Button from '@mui/material/Button';
import LinearProgress from '@mui/material/LinearProgress';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import type { ChangeEvent } from 'react';

import {
  EMPLOYEE_SORT_FIELDS,
  EMPLOYEE_TABLE_COLUMNS,
  type EmployeeSortField,
} from '../../constants/employeeConstants';
import { ACTION_LABELS, FIELD_LABELS, TABLE_LABELS } from '../../constants/messageConstants';
import { PAGE_SIZE_OPTIONS, type SortOrder } from '../../constants/paginationConstants';
import type { Employee } from '../../models/employee';
import { formatCurrency } from '../../utils/formatCurrency';

interface EmployeeTableProps {
  employees: Employee[];
  total: number;
  /** One-based page number, as the API uses. */
  page: number;
  pageSize: number;
  sortBy: EmployeeSortField;
  sortOrder: SortOrder;
  isLoading: boolean;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
  onSort: (field: EmployeeSortField) => void;
  onEdit: (employee: Employee) => void;
  onDelete: (employee: Employee) => void;
}

function cellValue(employee: Employee, field: EmployeeSortField): string {
  return field === EMPLOYEE_SORT_FIELDS.ANNUAL_SALARY
    ? formatCurrency(employee.annual_salary, employee.currency)
    : employee[field];
}

export default function EmployeeTable({
  employees,
  total,
  page,
  pageSize,
  sortBy,
  sortOrder,
  isLoading,
  onPageChange,
  onPageSizeChange,
  onSort,
  onEdit,
  onDelete,
}: EmployeeTableProps) {
  const columnCount = EMPLOYEE_TABLE_COLUMNS.length + 1;

  return (
    <Paper variant="outlined">
      {isLoading && <LinearProgress />}
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              {EMPLOYEE_TABLE_COLUMNS.map(({ field, align }) => (
                <TableCell key={field} align={align} sortDirection={sortBy === field && sortOrder}>
                  <TableSortLabel
                    active={sortBy === field}
                    direction={sortBy === field ? sortOrder : 'asc'}
                    onClick={() => onSort(field)}
                  >
                    {FIELD_LABELS[field]}
                  </TableSortLabel>
                </TableCell>
              ))}
              <TableCell align="right">{TABLE_LABELS.ACTIONS}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {employees.map((employee) => (
              <TableRow key={employee.id} hover>
                {EMPLOYEE_TABLE_COLUMNS.map(({ field, align }) => (
                  <TableCell key={field} align={align}>
                    {cellValue(employee, field)}
                  </TableCell>
                ))}
                <TableCell align="right" sx={{ whiteSpace: 'nowrap' }}>
                  <Button
                    size="small"
                    aria-label={`${ACTION_LABELS.EDIT} ${employee.full_name}`}
                    onClick={() => onEdit(employee)}
                  >
                    {ACTION_LABELS.EDIT}
                  </Button>
                  <Button
                    size="small"
                    color="error"
                    aria-label={`${ACTION_LABELS.DELETE} ${employee.full_name}`}
                    onClick={() => onDelete(employee)}
                  >
                    {ACTION_LABELS.DELETE}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
            {!isLoading && employees.length === 0 && (
              <TableRow>
                <TableCell colSpan={columnCount} align="center" sx={{ py: 6 }}>
                  {TABLE_LABELS.EMPTY}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={total}
        page={page - 1}
        rowsPerPage={pageSize}
        rowsPerPageOptions={[...PAGE_SIZE_OPTIONS]}
        labelRowsPerPage={TABLE_LABELS.ROWS_PER_PAGE}
        onPageChange={(_, zeroBasedPage) => onPageChange(zeroBasedPage + 1)}
        onRowsPerPageChange={(event: ChangeEvent<HTMLInputElement>) =>
          onPageSizeChange(Number(event.target.value))
        }
      />
    </Paper>
  );
}
