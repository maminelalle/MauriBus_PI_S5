import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/trips_provider.dart';
import '../providers/lines_provider.dart';
import '../widgets/trip_card.dart';
import '../widgets/custom_app_bar.dart';
import '../widgets/empty_state.dart';
import '../models/models.dart';

class TripsScreen extends StatefulWidget {
  final int lineId;
  final String lineName;

  const TripsScreen({
    Key? key,
    required this.lineId,
    required this.lineName,
  }) : super(key: key);

  @override
  State<TripsScreen> createState() => _TripsScreenState();
}

class _TripsScreenState extends State<TripsScreen> {
  late TripsProvider _tripsProvider;
  String _selectedFilter = 'all';

  @override
  void initState() {
    super.initState();
    _tripsProvider = context.read<TripsProvider>();
    _tripsProvider.fetchTrips(lineId: widget.lineId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: widget.lineName,
        showProfile: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Plus de détails bientôt')),
              );
            },
          ),
        ],
      ),
      body: Consumer<TripsProvider>(
        builder: (context, tripsProvider, _) {
          if (tripsProvider.isLoading) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (tripsProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.error_outline,
                    size: 64,
                    color: Colors.red[300],
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Erreur de chargement',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey[700],
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    tripsProvider.error ?? 'Erreur inconnue',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton(
                    onPressed: () {
                      tripsProvider.fetchTrips(lineId: widget.lineId);
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primaryColor,
                    ),
                    child: const Text(
                      'Réessayer',
                      style: TextStyle(color: Colors.white),
                    ),
                  ),
                ],
              ),
            );
          }

          final trips = tripsProvider.trips;

          if (trips.isEmpty) {
            return EmptyState(
              icon: Icons.directions_bus_filled_outlined,
              title: 'Aucun trajet disponible',
              subtitle: 'Il n\'y a actuellement aucun trajet pour cette ligne.',
              actionLabel: 'Retour',
              onActionTap: () => Navigator.pop(context),
            );
          }

          return RefreshIndicator(
            onRefresh: () => tripsProvider.fetchTrips(lineId: widget.lineId),
            color: AppTheme.primaryColor,
            child: Column(
              children: [
                // Filtres
                Padding(
                  padding: const EdgeInsets.all(AppTheme.paddingM),
                  child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        _FilterChip(
                          label: 'Tous',
                          isSelected: _selectedFilter == 'all',
                          onTap: () {
                            setState(() => _selectedFilter = 'all');
                            tripsProvider.filterByStatus('all');
                          },
                        ),
                        const SizedBox(width: 8),
                        _FilterChip(
                          label: 'En attente',
                          isSelected: _selectedFilter == 'pending',
                          onTap: () {
                            setState(() => _selectedFilter = 'pending');
                            tripsProvider.filterByStatus('pending');
                          },
                        ),
                        const SizedBox(width: 8),
                        _FilterChip(
                          label: 'En cours',
                          isSelected: _selectedFilter == 'ongoing',
                          onTap: () {
                            setState(() => _selectedFilter = 'ongoing');
                            tripsProvider.filterByStatus('ongoing');
                          },
                        ),
                        const SizedBox(width: 8),
                        _FilterChip(
                          label: 'Places libres',
                          isSelected: _selectedFilter == 'available',
                          onTap: () {
                            setState(() => _selectedFilter = 'available');
                            tripsProvider.filterByAvailability(true);
                          },
                        ),
                      ],
                    ),
                  ),
                ),
                // Liste des trajets
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppTheme.paddingM,
                      vertical: AppTheme.paddingS,
                    ),
                    itemCount: trips.length,
                    itemBuilder: (context, index) {
                      final trip = trips[index];
                      return TripCard(
                        trip: trip,
                        onTap: () {
                          tripsProvider.selectTrip(trip);
                          Navigator.pushNamed(context, '/booking', arguments: trip);
                        },
                      );
                    },
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _FilterChip({
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          gradient: isSelected
              ? const LinearGradient(
                  colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
                )
              : null,
          color: isSelected ? null : Colors.grey[200],
          borderRadius: BorderRadius.circular(AppTheme.radiusM),
          border: Border.all(
            color: isSelected
                ? Colors.transparent
                : Colors.grey[300]!,
            width: 1,
          ),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w600,
            color: isSelected ? Colors.white : Colors.grey[700],
          ),
        ),
      ),
    );
  }
}
