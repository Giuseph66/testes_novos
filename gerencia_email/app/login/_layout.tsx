import { Stack } from 'expo-router';

export default function LoginLayout() {
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
      <Stack.Screen name="index" options={{ headerShown: false }} />
    </Stack>
  );
} 