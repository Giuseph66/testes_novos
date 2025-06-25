import { Stack } from 'expo-router';
import { useColorScheme } from 'react-native';
import LoadingScreen from '../components/LoadingScreen';
import { AppProvider, useApp } from '../contexts/AppContext';

function RootLayoutNav() {
  const { isLoading } = useApp();

  if (isLoading) {
    return <LoadingScreen message="Conectando ao servidor..." />;
  }

  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: {
          backgroundColor: '#0a0a0a',
        },
        headerStyle: {
          backgroundColor: '#0a0a0a',
        },
      }}>
      <Stack.Screen name="login" options={{ headerShown: false }} />
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
  );
}

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <AppProvider>
      <RootLayoutNav />
    </AppProvider>
  );
}
