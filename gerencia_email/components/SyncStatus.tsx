import React, { useEffect, useState } from 'react';
import { Animated, StyleSheet, Text, View } from 'react-native';

interface SyncStatusProps {
  isOnline?: boolean;
  lastSync?: Date;
  isSyncing?: boolean;
}

export default function SyncStatus({ isOnline = true, lastSync, isSyncing = false }: SyncStatusProps) {
  const [pulseAnim] = useState(new Animated.Value(1));

  useEffect(() => {
    if (isOnline && !isSyncing) {
      const pulse = Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 0.7,
            duration: 1000,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 1000,
            useNativeDriver: true,
          }),
        ])
      );
      pulse.start();
      return () => pulse.stop();
    } else if (isSyncing) {
      // Animação mais rápida durante sincronização
      const pulse = Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 0.5,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          }),
        ])
      );
      pulse.start();
      return () => pulse.stop();
    }
  }, [isOnline, isSyncing, pulseAnim]);

  const getStatusText = () => {
    if (isSyncing) return 'Sincronizando...';
    if (isOnline) return 'Sincronizado';
    return 'Offline';
  };

  const getStatusColor = () => {
    if (isSyncing) return '#FFA500'; // Laranja durante sincronização
    if (isOnline) return '#4CAF50'; // Verde quando sincronizado
    return '#F44336'; // Vermelho quando offline
  };

  return (
    <View style={styles.container}>
      <View style={styles.statusContainer}>
        <Animated.View 
          style={[
            styles.statusDot, 
            { 
              backgroundColor: getStatusColor(),
              opacity: pulseAnim
            }
          ]} 
        />
        <Text style={styles.statusText}>
          {getStatusText()}
        </Text>
      </View>
      {lastSync && !isSyncing && (
        <Text style={styles.lastSyncText}>
          Última sincronização: {lastSync.toLocaleTimeString()}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: '#1a1a1a',
    borderTopWidth: 1,
    borderTopColor: '#333',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  statusText: {
    fontSize: 12,
    color: '#888',
    fontWeight: '500',
  },
  lastSyncText: {
    fontSize: 10,
    color: '#666',
  },
}); 