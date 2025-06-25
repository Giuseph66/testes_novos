import { router } from 'expo-router';
import React, { useEffect } from 'react';
import {
    FlatList,
    SafeAreaView,
    StatusBar,
    StyleSheet,
    Text,
    View,
} from 'react-native';
import { useApp } from '../../contexts/AppContext';

export default function RelatorioScreen() {
  const { emailAccounts, isAuthenticated } = useApp();

  // Redirecionar se não estiver autenticado
  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated]);

  const totalEmails = emailAccounts.length;
  const totalUses = emailAccounts.reduce((total, email) => total + email.uses.length, 0);
  const averageUsesPerEmail = totalEmails > 0 ? (totalUses / totalEmails).toFixed(1) : '0';

  const allUses = emailAccounts.flatMap(email => 
    email.uses.map(use => ({ use, email: email.email }))
  );

  const useCounts = allUses.reduce((acc, { use }) => {
    acc[use] = (acc[use] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const sortedUses = Object.entries(useCounts)
    .sort(([,a], [,b]) => b - a)
    .map(([use, count]) => ({ use, count }));

  // Se não estiver autenticado, não renderizar nada
  if (!isAuthenticated) {
    return null;
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0a0a0a" />
      
      <View style={styles.header}>
        <Text style={styles.title}>Relatório Geral</Text>
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{totalEmails}</Text>
          <Text style={styles.statLabel}>Total de E-mails</Text>
        </View>
        
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{totalUses}</Text>
          <Text style={styles.statLabel}>Total de Usos</Text>
        </View>
        
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{averageUsesPerEmail}</Text>
          <Text style={styles.statLabel}>Média por E-mail</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Usos Mais Frequentes</Text>
        {sortedUses.length > 0 ? (
          <FlatList
            data={sortedUses}
            keyExtractor={(item) => item.use}
            renderItem={({ item, index }) => (
              <View style={styles.useItem}>
                <View style={styles.rankContainer}>
                  <Text style={styles.rank}>#{index + 1}</Text>
                </View>
                <View style={styles.useInfo}>
                  <Text style={styles.useName}>{item.use}</Text>
                  <Text style={styles.useCount}>{item.count} e-mail{item.count > 1 ? 's' : ''}</Text>
                </View>
              </View>
            )}
            contentContainerStyle={styles.listContainer}
            showsVerticalScrollIndicator={false}
          />
        ) : (
          <View style={styles.emptyState}>
            <Text style={styles.emptyStateText}>Nenhum uso cadastrado</Text>
          </View>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Detalhes por E-mail</Text>
        {emailAccounts.length > 0 ? (
          <FlatList
            data={emailAccounts}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <View style={styles.emailItem}>
                <Text style={styles.emailAddress}>{item.email}</Text>
                <Text style={styles.emailUses}>
                  {item.uses.length} uso{item.uses.length !== 1 ? 's' : ''}
                </Text>
                {item.uses.length > 0 && (
                  <View style={styles.usesList}>
                    {item.uses.map((use, index) => (
                      <Text key={index} style={styles.useTag}>
                        {use}
                      </Text>
                    ))}
                  </View>
                )}
              </View>
            )}
            contentContainerStyle={styles.listContainer}
            showsVerticalScrollIndicator={false}
          />
        ) : (
          <View style={styles.emptyState}>
            <Text style={styles.emptyStateText}>Nenhum e-mail cadastrado</Text>
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  header: {
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  statsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    paddingVertical: 16,
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#333',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: '#888',
    textAlign: 'center',
  },
  section: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 16,
  },
  listContainer: {
    paddingBottom: 20,
  },
  useItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1a1a1a',
    borderRadius: 12,
    padding: 16,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: '#333',
  },
  rankContainer: {
    backgroundColor: '#007AFF',
    borderRadius: 20,
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  rank: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  useInfo: {
    flex: 1,
  },
  useName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
    marginBottom: 4,
  },
  useCount: {
    fontSize: 14,
    color: '#888',
  },
  emailItem: {
    backgroundColor: '#1a1a1a',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#333',
  },
  emailAddress: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
    marginBottom: 4,
  },
  emailUses: {
    fontSize: 14,
    color: '#888',
    marginBottom: 8,
  },
  usesList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  useTag: {
    backgroundColor: '#007AFF',
    color: '#ffffff',
    fontSize: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
}); 