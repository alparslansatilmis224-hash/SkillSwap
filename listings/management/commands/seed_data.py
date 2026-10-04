from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Category, SkillListing
from swaps.models import SwapRequest

User = get_user_model()


class Command(BaseCommand):
    help = 'SkillSwap veritabanını örnek kategori, kullanıcı, ilan ve takas teklifleriyle doldurur.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("SkillSwap örnek verileri yükleniyor..."))

        # 1. Admin Kullanıcısı
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@skillswap.local',
                'first_name': 'Sistem',
                'last_name': 'Yöneticisi',
                'is_staff': True,
                'is_superuser': True,
                'location': 'İstanbul',
                'bio': 'SkillSwap Platform Yöneticisi'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Admin kullanıcısı oluşturuldu: admin / admin123"))

        # 2. Örnek Kullanıcılar
        users_data = [
            {
                'username': 'ahmet_dev',
                'email': 'ahmet@example.com',
                'first_name': 'Ahmet',
                'last_name': 'Yılmaz',
                'location': 'İstanbul',
                'bio': '7 yıllık Full-Stack Web Geliştiriciyim. Python, Django ve Vue.js konularında uzmanım. Karşılığında akustik gitar veya İtalyanca öğrenmek istiyorum.',
                'password': 'password123'
            },
            {
                'username': 'ayse_design',
                'email': 'ayse@example.com',
                'first_name': 'Ayşe',
                'last_name': 'Demir',
                'location': 'Ankara',
                'bio': 'Freelance UI/UX ve Grafik Tasarımcısıyım. Figma, Adobe Illustrator ve marka kimliği tasarımı öğretebilirim. Python veya veri bilimi temelleri öğrenmek istiyorum.',
                'password': 'password123'
            },
            {
                'username': 'mehmet_guitar',
                'email': 'mehmet@example.com',
                'first_name': 'Mehmet',
                'last_name': 'Kaya',
                'location': 'İzmir',
                'bio': '10 yıldır klasik ve akustik gitar çalıyorum, müzik teorisi ve ritim dersleri veriyorum. Web sitesi kurmayı veya SEO tekniklerini öğrenmek isterim.',
                'password': 'password123'
            },
            {
                'username': 'elif_english',
                'email': 'elif@example.com',
                'first_name': 'Elif',
                'last_name': 'Çelik',
                'location': 'Online / Eskişehir',
                'bio': 'Mütercim tercümanlık mezunuyum. C1 seviyesinde İngilizce ve B2 İspanyolca konuşma pratiği yaptırabilirim. Karşılığında temel video montajı (Premiere Pro) arıyorum.',
                'password': 'password123'
            }
        ]

        created_users = {}
        for u_info in users_data:
            pwd = u_info.pop('password')
            u, c = User.objects.get_or_create(username=u_info['username'], defaults=u_info)
            if c:
                u.set_password(pwd)
                u.save()
            created_users[u.username] = u

        # 3. Kategoriler
        categories_data = [
            {'name': 'Yazılım & Web Geliştirme', 'description': 'Python, Django, JavaScript, React, Mobil Uygulama ve Veri Tabanı eğitimleri.'},
            {'name': 'Yabancı Dil & Konuşma', 'description': 'İngilizce, Almanca, İspanyolca konuşma pratiği, telaffuz ve sınav hazırlığı.'},
            {'name': 'Görsel Tasarım & UI/UX', 'description': 'Figma, Adobe XD, Photoshop, Logo Tasarımı, Tipografi ve Kullanıcı Deneyimi.'},
            {'name': 'Müzik & Enstrüman', 'description': 'Gitar, Piyano, Şan Eğitimi, Müzik Teorisi ve Ses Prodüksiyonu.'},
            {'name': 'Dijital Pazarlama & SEO', 'description': 'Arama motoru optimizasyonu, Google Ads, Sosyal Medya Yönetimi ve İçerik Üretimi.'},
            {'name': 'Fotoğraf & Video Kurgu', 'description': 'Premiere Pro, DaVinci Resolve, Temel Fotoğrafçılık ve Işık Teknikleri.'},
        ]

        created_categories = {}
        for cat in categories_data:
            c, _ = Category.objects.get_or_create(name=cat['name'], defaults={'description': cat['description']})
            created_categories[c.name] = c

        # 4. Yetenek İlanları
        listings_data = [
            {
                'title': 'Sıfırdan İleri Seviyeye Django ile Web Uygulamaları Geliştirme',
                'category': created_categories['Yazılım & Web Geliştirme'],
                'provider': created_users['ahmet_dev'],
                'difficulty_level': 'intermediate',
                'description': 'Django ORM, Class-Based Views, REST API mantığı ve veritabanı modellemesini birebir uygulamalı projeler üzerinden öğretiyorum. Karşılığında haftada 1-2 saat gitar akorları veya müzik teorisi çalışmak istiyorum.'
            },
            {
                'title': 'Figma ile Modern UI/UX Tasarım ve Prototipleme Temelleri',
                'category': created_categories['Görsel Tasarım & UI/UX'],
                'provider': created_users['ayse_design'],
                'difficulty_level': 'beginner',
                'description': 'Tasarım sistemleri, Auto Layout, Components, wireframe ve prototip oluşturmayı adım adım birlikte deneyimleyelim. Karşılığında Python programlama veya web geliştirme temelleri öğretecek bir takas arkadaşı arıyorum.'
            },
            {
                'title': 'Akustik & Klasik Gitar Başlangıç ve Ritim Eğitimi',
                'category': created_categories['Müzik & Enstrüman'],
                'provider': created_users['mehmet_guitar'],
                'difficulty_level': 'beginner',
                'description': 'Temel akorlar, arpejler, ritim kalıpları ve en sevdiğiniz şarkıları çalabilme garantisi! Müzik kulağınızı geliştirelim. Karşılığında web sitesi optimizasyonu veya sosyal medya büyüme stratejisi öğrenmek istiyorum.'
            },
            {
                'title': 'Akıcı İngilizce Konuşma Pratiği & IELTS/TOEFL Stratejileri',
                'category': created_categories['Yabancı Dil & Konuşma'],
                'provider': created_users['elif_english'],
                'difficulty_level': 'intermediate',
                'description': 'Günlük konuşma bariyerinizi yıkacak interaktif seanslar, idiomlar ve telaffuz düzeltmeleri. Karşılığında YouTube için video kurgulama (Premiere veya DaVinci) öğretebilecek birisini arıyorum.'
            },
            {
                'title': 'İleri Düzey Python: AsyncIO, Metaprogramming ve Temiz Kod',
                'category': created_categories['Yazılım & Web Geliştirme'],
                'provider': created_users['ahmet_dev'],
                'difficulty_level': 'advanced',
                'description': 'Büyük ölçekli Python projeleri için mimari desenler, asyncio, threading ve test odaklı geliştirme (TDD). Karşılığında ileri seviye Figma veya ürün tasarımı mentörlüğü arıyorum.'
            },
            {
                'title': 'Sosyal Medya Büyüme Stratejileri ve Etkili İçerik Planlama',
                'category': created_categories['Dijital Pazarlama & SEO'],
                'provider': created_users['ayse_design'],
                'difficulty_level': 'beginner',
                'description': 'Instagram ve LinkedIn algoritmalarını anlama, organik takipçi kazanımı, etkileşim artıran görsel şablonlar hazırlama. Karşılığında temel düzeyde İngilizce telaffuz desteği rica ediyorum.'
            },
        ]

        created_listings = []
        for l_data in listings_data:
            listing, _ = SkillListing.objects.get_or_create(
                title=l_data['title'],
                provider=l_data['provider'],
                defaults=l_data
            )
            created_listings.append(listing)

        # 5. Örnek Takas Teklifleri
        if len(created_listings) >= 2:
            # Mehmet -> Ahmet'in Django ilanına takas teklif ediyor
            SwapRequest.objects.get_or_create(
                listing=created_listings[0],
                requester=created_users['mehmet_guitar'],
                defaults={
                    'message': 'Selam Ahmet! Django öğrenmeyi çok istiyorum çünkü müzik arşivim için bir web sitesi yapma hayalim var. Sana haftada 2 saat gitar ve armoni öğretebilirim, ne dersin?',
                    'status': 'pending'
                }
            )

            # Elif -> Ayşe'nin Figma ilanına teklif ediyor
            SwapRequest.objects.get_or_create(
                listing=created_listings[1],
                requester=created_users['elif_english'],
                defaults={
                    'message': 'Merhaba Ayşe! Figma arayüz tasarımını portfolyom için öğrenmek istiyorum. Karşılığında seninle haftalık İngilizce speaking pratiği yapabiliriz. Çok verimli olacağına eminim!',
                    'status': 'accepted'
                }
            )

        self.stdout.write(self.style.SUCCESS("✓ Başarıyla örnek veriler eklendi!"))
        self.stdout.write(self.style.SUCCESS("Demo Kullanıcılar: ahmet_dev, ayse_design, mehmet_guitar, elif_english (Şifre: password123)"))
        self.stdout.write(self.style.SUCCESS("Admin Paneli: admin / admin123"))
