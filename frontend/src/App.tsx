import { BrowserRouter, Routes, Route } from 'react-router';
import { Shell } from '@/components/layout/Shell';
import { OperationsPage } from '@/pages/OperationsPage';
import {
  IncidentsPage,
  DevicesPage,
  ServicesPage,
  AnalyticsPage,
  AuditPage,
  SettingsPage,
} from '@/pages/Placeholders';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Shell />}>
          <Route index element={<OperationsPage />} />
          <Route path="incidents" element={<IncidentsPage />} />
          <Route path="devices" element={<DevicesPage />} />
          <Route path="services" element={<ServicesPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="audit" element={<AuditPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
