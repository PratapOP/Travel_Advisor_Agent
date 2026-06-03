from django.core.management.base import BaseCommand
from emergency.models import EmergencyContact
from hotels.models import Hotel
from tourism.models import PhotoPose, TouristSpot

class Command(BaseCommand):
    help = 'Seeds the database with premium travel sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with Travel Adviser Agent data...')
        
        # 1. Seed Emergency Contacts
        EmergencyContact.objects.all().delete()
        emergency_data = [
            # France
            {"country": "France", "city": "Paris", "police_contact": "17", "ambulance_contact": "15", "tourist_helpline": "+33 1 45 50 34 75", "embassy_contact": "US Embassy: +33 1 43 12 22 22"},
            # Japan
            {"country": "Japan", "city": "Tokyo", "police_contact": "110", "ambulance_contact": "119", "tourist_helpline": "+81 3 3201 3331", "embassy_contact": "US Embassy: +81 3 3224 5000"},
            # USA
            {"country": "United States", "city": "New York", "police_contact": "911", "ambulance_contact": "911", "tourist_helpline": "311", "embassy_contact": "Embassy Liaison: +1 212 963 1234"},
            # UK
            {"country": "United Kingdom", "city": "London", "police_contact": "999", "ambulance_contact": "999", "tourist_helpline": "+44 20 7604 8877", "embassy_contact": "US Embassy: +44 20 7499 9000"},
            # India
            {"country": "India", "city": "New Delhi", "police_contact": "112", "ambulance_contact": "102", "tourist_helpline": "1363", "embassy_contact": "US Embassy: +91 11 2419 8000"}
        ]
        for data in emergency_data:
            EmergencyContact.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(emergency_data)} emergency contact profiles.'))

        # 2. Seed Hotels
        Hotel.objects.all().delete()
        hotel_data = [
            # Paris
            {
                "hotel_name": "Hotel Ritz Paris", "city": "Paris", "country": "France", 
                "rating": 5.0, "price_per_night": 950.00, 
                "contact_email": "reservations@ritzparis.com", "contact_number": "+33 1 43 16 30 30",
                "latitude": 48.8681, "longitude": 2.3294
            },
            {
                "hotel_name": "Hotel de l'Esperance", "city": "Paris", "country": "France", 
                "rating": 4.4, "price_per_night": 160.00, 
                "contact_email": "contact@hotelesperance.fr", "contact_number": "+33 1 47 07 10 99",
                "latitude": 48.8398, "longitude": 2.3482
            },
            {
                "hotel_name": "Generator Paris Hostel", "city": "Paris", "country": "France", 
                "rating": 4.1, "price_per_night": 45.00, 
                "contact_email": "paris@generatorhostels.com", "contact_number": "+33 1 70 98 84 00",
                "latitude": 48.8786, "longitude": 2.3705
            },
            # Tokyo
            {
                "hotel_name": "Aman Tokyo", "city": "Tokyo", "country": "Japan", 
                "rating": 5.0, "price_per_night": 1250.00, 
                "contact_email": "amantokyo@aman.com", "contact_number": "+81 3 5224 3333",
                "latitude": 35.6848, "longitude": 139.7645
            },
            {
                "hotel_name": "Hotel Sunroute Plaza Shinjuku", "city": "Tokyo", "country": "Japan", 
                "rating": 4.3, "price_per_night": 180.00, 
                "contact_email": "shinjuku@sunrouteplaza.jp", "contact_number": "+81 3 3375 3211",
                "latitude": 35.6881, "longitude": 139.6997
            },
            {
                "hotel_name": "Grids Tokyo Ueno Hotel & Hostel", "city": "Tokyo", "country": "Japan", 
                "rating": 4.0, "price_per_night": 38.00, 
                "contact_email": "ueno@gridshostel.com", "contact_number": "+81 3 5830 0030",
                "latitude": 35.7144, "longitude": 139.7801
            },
            # New York
            {
                "hotel_name": "The Plaza Hotel", "city": "New York", "country": "United States", 
                "rating": 4.9, "price_per_night": 850.00, 
                "contact_email": "plazareservations@fairmont.com", "contact_number": "+1 212 759 3000",
                "latitude": 40.7644, "longitude": -73.9744
            },
            {
                "hotel_name": "Pod 39 Hotel Midtown", "city": "New York", "country": "United States", 
                "rating": 4.2, "price_per_night": 155.00, 
                "contact_email": "info@thepodhotel.com", "contact_number": "+1 212 865 3900",
                "latitude": 40.7494, "longitude": -73.9772
            },
            {
                "hotel_name": "Freehand New York East Village", "city": "New York", "country": "United States", 
                "rating": 4.1, "price_per_night": 85.00, 
                "contact_email": "ny@freehandhotels.com", "contact_number": "+1 212 475 1070",
                "latitude": 40.7386, "longitude": -73.9840
            }
        ]
        for data in hotel_data:
            Hotel.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(hotel_data)} hotel profiles.'))

        # 3. Seed Photo Poses
        PhotoPose.objects.all().delete()
        pose_data = [
            {"category": "solo", "description": "The Classic Looking Back: Walk slowly away from the camera, then turn your head back over your shoulder with a natural smile.", "image_reference": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80"},
            {"category": "solo", "description": "The Edge of the World: Sit on an elevated ledge or bench overlooking a city skyline, looking thoughtfully out at the view.", "image_reference": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"},
            {"category": "couple", "description": "Follow Me To: One partner holds the other's hand, leading them toward a famous monument, shot from the trailing partner's perspective.", "image_reference": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?auto=format&fit=crop&w=400&q=80"},
            {"category": "couple", "description": "Sunset Embrace: Backlit silhouette of the couple embracing against a golden hour sunset behind a historic monument.", "image_reference": "https://images.unsplash.com/photo-1464746133101-a2c3f88e0dd9?auto=format&fit=crop&w=400&q=80"},
            {"category": "family", "description": "Candid Walking: The family holds hands and walks together towards the camera, laughing and talking naturally.", "image_reference": "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?auto=format&fit=crop&w=400&q=80"},
            {"category": "family", "description": "The Landmark V-Shape: Stand together in a wedge formation in front of the landmark, with children in front and parents behind.", "image_reference": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=400&q=80"},
            {"category": "adventure", "description": "The Summit Jump: Mid-air action shot of you jumping on top of a mountain summit or high cliff, arms wide open.", "image_reference": "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=400&q=80"},
            {"category": "adventure", "description": "Action Perspective: POV shot looking down at your hiking boots at the edge of a canyon or looking forward on a kayak.", "image_reference": "https://images.unsplash.com/photo-1527631746610-bca00a040d60?auto=format&fit=crop&w=400&q=80"}
        ]
        for data in pose_data:
            PhotoPose.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(pose_data)} travel poses.'))

        # 4. Seed Tourist Spots
        TouristSpot.objects.all().delete()
        spot_data = [
            # Paris
            {
                "name": "Eiffel Tower", "city": "Paris", "country": "France",
                "description": "The quintessential icon of Paris. Visit at sunset to see the lights sparkle on the hour.",
                "category": "Popular Attraction", "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "La Petite Ceinture", "city": "Paris", "country": "France",
                "description": "An abandoned railway line reclaimed by nature. A peaceful hidden walkway away from tourists.",
                "category": "Hidden Gem", "rating": 4.5, "image_url": "https://images.unsplash.com/photo-1504198453319-5ce911bafcde?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Rue de l'Abreuvoir", "city": "Paris", "country": "France",
                "description": "The most beautiful street in Montmartre. Position yourself near the Maison Rose for a stunning photography background.",
                "category": "Best Photography Location", "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1508193638397-1c4234db14d8?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Artisanal Cheese & Wine Pairing", "city": "Paris", "country": "France",
                "description": "Spend an afternoon in a 17th-century cellar in Marais tasting hand-made French cheeses and organic wines.",
                "category": "Local Experience", "rating": 4.9, "image_url": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=400&q=80"
            },
            # Tokyo
            {
                "name": "Shibuya Crossing & Hachiko Statue", "city": "Tokyo", "country": "Japan",
                "description": "The busiest pedestrian crossing in the world. Best viewed from an elevated cafe window.",
                "category": "Popular Attraction", "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Todoroki Valley", "city": "Tokyo", "country": "Japan",
                "description": "A forested ravine right in the middle of Tokyo. Cross the red bridge to explore walking paths and ancient shrines.",
                "category": "Hidden Gem", "rating": 4.4, "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Omoide Yokocho (Memory Lane)", "city": "Tokyo", "country": "Japan",
                "description": "Alleyway in Shinjuku with lantern-lit yakitori stalls. Best photography spots are under the seasonal artificial blossoms.",
                "category": "Best Photography Location", "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Traditional Tea Ceremony", "city": "Tokyo", "country": "Japan",
                "description": "Participate in a mindful tea preparation workshop under a Master in a historical garden.",
                "category": "Local Experience", "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=400&q=80"
            },
            # New York
            {
                "name": "Central Park & Bethesda Terrace", "city": "New York", "country": "United States",
                "description": "The green lung of NYC. Bethesda Terrace offers grand arches and views of the lake.",
                "category": "Popular Attraction", "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1518235506717-e1ed3306a89b?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Roosevelt Island Tramway", "city": "New York", "country": "United States",
                "description": "Take a cable car ride alongside the Queensboro Bridge for spectacular skyline views for the cost of a subway swipe.",
                "category": "Hidden Gem", "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1485738422979-f5c462d49f74?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "DUMBO (Washington Street View)", "city": "New York", "country": "United States",
                "description": "Iconic framing of the Manhattan Bridge between red-brick warehouses. Shoot from a low angle for dramatic perspective.",
                "category": "Best Photography Location", "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Broadway Behind-The-Scenes Tour", "city": "New York", "country": "United States",
                "description": "Walk through historic theatres, talk with actors, and understand the technical magic of a Broadway show.",
                "category": "Local Experience", "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?auto=format&fit=crop&w=400&q=80"
            }
        ]
        for data in spot_data:
            TouristSpot.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(spot_data)} tourist spots.'))
        
        self.stdout.write(self.style.SUCCESS('All travel data has been successfully seeded!'))
