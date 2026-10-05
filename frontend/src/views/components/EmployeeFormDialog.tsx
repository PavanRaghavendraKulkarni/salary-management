import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Grid2';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import type { FormEvent } from 'react';

import { EMPLOYEE_FORM_MODES, type EmployeeFormMode } from '../../constants/employeeConstants';
import { ACTION_LABELS, DIALOG_TITLES, FIELD_LABELS } from '../../constants/messageConstants';
import type { EmployeeFormErrors } from '../../controllers/employeeFormValidation';
import type { EmployeeInput, ReferenceData } from '../../models/employee';
import { todayIsoDate } from '../../utils/todayIsoDate';

interface EmployeeFormDialogProps {
  isOpen: boolean;
  mode: EmployeeFormMode;
  values: EmployeeInput;
  errors: EmployeeFormErrors;
  submitError: string | null;
  isSubmitting: boolean;
  referenceData: ReferenceData | null;
  onChange: (name: keyof EmployeeInput, value: string) => void;
  onSubmit: () => void;
  onClose: () => void;
}

export default function EmployeeFormDialog({
  isOpen,
  mode,
  values,
  errors,
  submitError,
  isSubmitting,
  referenceData,
  onChange,
  onSubmit,
  onClose,
}: EmployeeFormDialogProps) {
  const title = mode === EMPLOYEE_FORM_MODES.EDIT ? DIALOG_TITLES.EDIT : DIALOG_TITLES.CREATE;

  const fieldProps = (name: keyof EmployeeInput) => ({
    id: `employee-${name}`,
    label: FIELD_LABELS[name],
    value: values[name],
    error: Boolean(errors[name]),
    helperText: errors[name] ?? ' ',
    fullWidth: true,
    size: 'small' as const,
    onChange: (event: { target: { value: string } }) => onChange(name, event.target.value),
  });

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <Dialog open={isOpen} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit} noValidate>
        <DialogTitle>{title}</DialogTitle>
        <DialogContent>
          {submitError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {submitError}
            </Alert>
          )}
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField {...fieldProps('full_name')} required autoFocus />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField {...fieldProps('email')} required type="email" />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField {...fieldProps('job_title')} required select>
                {referenceData?.job_titles.map((jobTitle) => (
                  <MenuItem key={jobTitle} value={jobTitle}>
                    {jobTitle}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField {...fieldProps('department')} required select>
                {referenceData?.departments.map((department) => (
                  <MenuItem key={department} value={department}>
                    {department}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 8 }}>
              <TextField {...fieldProps('country')} required select>
                {referenceData?.countries.map((country) => (
                  <MenuItem key={country.name} value={country.name}>
                    {country.name}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <TextField
                {...fieldProps('currency')}
                slotProps={{ htmlInput: { readOnly: true } }}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                {...fieldProps('annual_gross_salary')}
                required
                slotProps={{ htmlInput: { inputMode: 'decimal' } }}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                {...fieldProps('hire_date')}
                required
                type="date"
                slotProps={{ inputLabel: { shrink: true }, htmlInput: { max: todayIsoDate() } }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>{ACTION_LABELS.CANCEL}</Button>
          <Button type="submit" variant="contained" disabled={isSubmitting}>
            {ACTION_LABELS.SAVE}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
