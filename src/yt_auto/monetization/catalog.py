"""Catálogo curado de programas de afiliados (multi-nicho).

⚠️ ADVERTENCIA SOBRE LA FIABILIDAD DE ESTOS DATOS:

1. **Los CPA son ESTIMACIONES** de investigación con agentes (2026), no
   contratos verificados. Verifica las condiciones reales al registrarte
   en cada programa antes de citar cifras en contenido o proyecciones.
2. **Los `affiliate_url_template` son formatos PLACEHOLDER inventados.**
   La estructura real del enlace la entrega el dashboard de cada programa
   al darte de alta (a menudo vía Impact, PartnerStack, FirstPromoter...).
   NUNCA publiques estos templates tal cual: sustituye la URL completa
   por tu enlace real de afiliado y conserva solo los parámetros UTM.

Para añadir un programa nuevo: añade un `AffiliateProgram` a la lista
`AFFILIATE_CATALOG` y referéncialo desde el `affiliate_focus` del perfil
de nicho YAML correspondiente.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from yt_auto.publishing.niche_profile import NicheProfile

ProgramCategory = Literal[
    "credit_builder",
    "credit_card",
    "real_estate",
    "tax_software",
    "small_business_banking",
    "payroll_bookkeeping",
    "credit_history_translation",
    "investing",
    "automation_saas",
    "ai_tool",
    "hosting_vps",
    "crm_realestate",
]


class AffiliateProgram(BaseModel):
    """Un programa de afiliados curado y verificable."""

    id: str = Field(..., description="Slug interno, ej. 'self_financial'")
    display_name: str
    category: ProgramCategory
    landing_url: HttpUrl = Field(..., description="URL pública del programa")
    affiliate_url_template: str = Field(
        ...,
        description=(
            "Plantilla con `{utm}` substituible. Ejemplo: "
            "'https://www.self.inc/?ref=tucanal&{utm}'"
        ),
    )
    cpa_usd_min: float = Field(..., ge=0)
    cpa_usd_max: float = Field(..., ge=0)
    cpa_model: Literal[
        "per_signup", "per_approval", "per_funded_loan", "per_referral", "recurring"
    ]
    recurring_months: int = Field(
        0, ge=0, description="Meses de comisión recurrente (0 si es pago único)"
    )
    cookie_days: int = 30
    spanish_landing_available: bool = False
    notes_es: str = ""


AFFILIATE_CATALOG: list[AffiliateProgram] = [
    # --- Credit Builders ---
    AffiliateProgram(
        id="self_financial",
        display_name="Self Financial (Credit Builder Loan)",
        category="credit_builder",
        landing_url="https://www.self.inc/",
        affiliate_url_template="https://www.self.inc/?ref=tucanal&{utm}",
        cpa_usd_min=10,
        cpa_usd_max=30,
        cpa_model="per_funded_loan",
        spanish_landing_available=True,
        notes_es="Conversión muy alta en audiencia inmigrante. Producto core del nicho ITIN.",
    ),
    AffiliateProgram(
        id="kikoff",
        display_name="Kikoff (Credit Builder)",
        category="credit_builder",
        landing_url="https://kikoff.com/",
        affiliate_url_template="https://kikoff.com/refer/tucanal?{utm}",
        cpa_usd_min=15,
        cpa_usd_max=35,
        cpa_model="per_signup",
        notes_es="No requiere SSN obligatorio. Buen complement de Self.",
    ),
    AffiliateProgram(
        id="chime_credit_builder",
        display_name="Chime Credit Builder Card",
        category="credit_builder",
        landing_url="https://www.chime.com/credit-builder/",
        affiliate_url_template="https://chime.com/r/tucanal?{utm}",
        cpa_usd_min=15,
        cpa_usd_max=40,
        cpa_model="per_signup",
        spanish_landing_available=True,
    ),
    # --- Secured cards / ITIN cards ---
    AffiliateProgram(
        id="capital_one_platinum_secured",
        display_name="Capital One Platinum Secured (ITIN-friendly)",
        category="credit_card",
        landing_url="https://www.capitalone.com/credit-cards/platinum-secured/",
        affiliate_url_template="https://i.capitalone.com/r/tucanal?{utm}",
        cpa_usd_min=20,
        cpa_usd_max=60,
        cpa_model="per_approval",
        spanish_landing_available=True,
        notes_es="Capital One acepta ITIN. Producto tradicional para empezar crédito.",
    ),
    AffiliateProgram(
        id="nova_credit",
        display_name="Nova Credit (Credit History Translation)",
        category="credit_history_translation",
        landing_url="https://www.novacredit.com/",
        affiliate_url_template="https://www.novacredit.com/r/tucanal?{utm}",
        cpa_usd_min=25,
        cpa_usd_max=75,
        cpa_model="per_referral",
        notes_es=(
            "INFRAUTILIZADO. Programa específico para creadores hispanos; "
            "permite a inmigrantes 'traer' su historial crediticio de origen."
        ),
    ),
    AffiliateProgram(
        id="alterna_card",
        display_name="Alterna Card (Credit for Non-Residents)",
        category="credit_card",
        landing_url="https://www.alternacard.com/",
        affiliate_url_template="https://www.alternacard.com/r/tucanal?{utm}",
        cpa_usd_min=30,
        cpa_usd_max=80,
        cpa_model="per_approval",
        spanish_landing_available=True,
        notes_es=(
            "Programa de afiliados específico para audiencia hispana "
            "inmigrante. Poco saturado."
        ),
    ),
    # --- Real Estate ---
    AffiliateProgram(
        id="stessa",
        display_name="Stessa (Property Management Software)",
        category="real_estate",
        landing_url="https://www.stessa.com/",
        affiliate_url_template="https://www.stessa.com/affiliate/tucanal?{utm}",
        cpa_usd_min=120,
        cpa_usd_max=120,
        cpa_model="per_signup",
        cookie_days=90,
        notes_es="$120/referido + cookie 90 días. Para audiencia compradora-inversora.",
    ),
    AffiliateProgram(
        id="doorloop",
        display_name="DoorLoop (Property Management)",
        category="real_estate",
        landing_url="https://www.doorloop.com/",
        affiliate_url_template="https://www.doorloop.com/affiliate/tucanal?{utm}",
        cpa_usd_min=50,
        cpa_usd_max=250,
        cpa_model="per_referral",
        notes_es="Hasta $250/cliente para audiencia que compra para alquilar.",
    ),
    AffiliateProgram(
        id="rocket_mortgage",
        display_name="Rocket Mortgage (Affiliate)",
        category="real_estate",
        landing_url="https://www.rocketmortgage.com/",
        affiliate_url_template="https://www.rocketmortgage.com/affiliate/tucanal?{utm}",
        cpa_usd_min=50,
        cpa_usd_max=200,
        cpa_model="per_funded_loan",
        spanish_landing_available=True,
        notes_es="Programas para inmigrantes/ITIN. Verifica disponibilidad en tu estado.",
    ),
    # --- Tax software ---
    AffiliateProgram(
        id="taxslayer_pro",
        display_name="TaxSlayer Pro (B2B tax preparers)",
        category="tax_software",
        landing_url="https://www.taxslayerpro.com/",
        affiliate_url_template="https://www.taxslayerpro.com/affiliate/tucanal?{utm}",
        cpa_usd_min=20,
        cpa_usd_max=100,
        cpa_model="per_signup",
        notes_es="Alianza visible con Latino Tax Pro. Audiencia preparadores hispanos.",
    ),
    AffiliateProgram(
        id="turbotax_es",
        display_name="TurboTax (Spanish version)",
        category="tax_software",
        landing_url="https://turbotax.intuit.com/personal-taxes/online/spanish/",
        affiliate_url_template="https://turbotax.intuit.com/r/tucanal?{utm}",
        cpa_usd_min=15,
        cpa_usd_max=50,
        cpa_model="per_signup",
        spanish_landing_available=True,
        notes_es="Conversión alta Q1 (enero-abril). RPM pico estacional.",
    ),
    # --- Small Business Banking ---
    AffiliateProgram(
        id="mercury",
        display_name="Mercury (Banking for non-resident LLCs)",
        category="small_business_banking",
        landing_url="https://mercury.com/",
        affiliate_url_template="https://mercury.com/r/tucanal?{utm}",
        cpa_usd_min=50,
        cpa_usd_max=200,
        cpa_model="per_approval",
        notes_es="Popular en audiencia immigrant founder. Acepta non-resident LLCs.",
    ),
    AffiliateProgram(
        id="novo",
        display_name="Novo (Small Business Banking)",
        category="small_business_banking",
        landing_url="https://www.novo.co/",
        affiliate_url_template="https://www.novo.co/r/tucanal?{utm}",
        cpa_usd_min=20,
        cpa_usd_max=50,
        cpa_model="per_approval",
        notes_es="Banking sin SSN. Conversión decente en audiencia LLC.",
    ),
    AffiliateProgram(
        id="bluevine",
        display_name="Bluevine (Business Banking + Credit)",
        category="small_business_banking",
        landing_url="https://www.bluevine.com/",
        affiliate_url_template="https://www.bluevine.com/r/tucanal?{utm}",
        cpa_usd_min=30,
        cpa_usd_max=100,
        cpa_model="per_approval",
    ),
    # --- Payroll & Bookkeeping ---
    AffiliateProgram(
        id="gusto",
        display_name="Gusto (Payroll)",
        category="payroll_bookkeeping",
        landing_url="https://gusto.com/",
        affiliate_url_template="https://gusto.com/r/tucanal?{utm}",
        cpa_usd_min=150,
        cpa_usd_max=300,
        cpa_model="per_referral",
        notes_es="CPA alto, conversión alta en LLCs con empleados.",
    ),
    AffiliateProgram(
        id="quickbooks",
        display_name="QuickBooks (Small Business Accounting)",
        category="payroll_bookkeeping",
        landing_url="https://quickbooks.intuit.com/",
        affiliate_url_template="https://quickbooks.intuit.com/r/tucanal?{utm}",
        cpa_usd_min=5,
        cpa_usd_max=25,
        cpa_model="per_signup",
        spanish_landing_available=True,
    ),
    AffiliateProgram(
        id="bench",
        display_name="Bench (Outsourced Bookkeeping)",
        category="payroll_bookkeeping",
        landing_url="https://bench.co/",
        affiliate_url_template="https://bench.co/r/tucanal?{utm}",
        cpa_usd_min=100,
        cpa_usd_max=300,
        cpa_model="per_referral",
    ),
    # --- H&R Block ---
    AffiliateProgram(
        id="h_and_r_block",
        display_name="H&R Block (Tax filing, Spanish)",
        category="tax_software",
        landing_url="https://www.hrblock.com/",
        affiliate_url_template="https://www.hrblock.com/r/tucanal?{utm}",
        cpa_usd_min=10,
        cpa_usd_max=40,
        cpa_model="per_signup",
        spanish_landing_available=True,
    ),
    # --- Investing ---
    AffiliateProgram(
        id="roofstock",
        display_name="Roofstock (Real Estate Investment)",
        category="investing",
        landing_url="https://www.roofstock.com/",
        affiliate_url_template="https://www.roofstock.com/r/tucanal?{utm}",
        cpa_usd_min=15,
        cpa_usd_max=500,
        cpa_model="per_signup",
        notes_es="Marketplace de inversión inmobiliaria. CPA escala por activación.",
    ),
    AffiliateProgram(
        id="mytaxprepoffice",
        display_name="MyTAXPrepOffice (Tax software pro)",
        category="tax_software",
        landing_url="https://www.mytaxprepoffice.com/",
        affiliate_url_template="https://www.mytaxprepoffice.com/r/tucanal?{utm}",
        cpa_usd_min=25,
        cpa_usd_max=100,
        cpa_model="per_signup",
        notes_es="Audiencia avanzada/preparadores profesionales.",
    ),
    # ==================================================================
    # Automatización IA (nicho: automatización IA para inmobiliarias)
    # Afiliados con comisión RECURRENTE = la columna vertebral del nicho.
    # ==================================================================
    AffiliateProgram(
        id="make",
        display_name="Make.com (Automatización no-code)",
        category="automation_saas",
        landing_url="https://www.make.com/",
        affiliate_url_template="https://www.make.com/en/register?pc=tucanal&{utm}",
        cpa_usd_min=20,
        cpa_usd_max=200,
        cpa_model="recurring",
        recurring_months=12,
        notes_es=(
            "35% comisión durante 12 meses. Se muestra en pantalla en cada "
            "tutorial = conversión natural."
        ),
    ),
    AffiliateProgram(
        id="n8n_cloud",
        display_name="n8n Cloud (Automatización open-source)",
        category="automation_saas",
        landing_url="https://n8n.io/",
        affiliate_url_template="https://n8n.io/?ref=tucanal&{utm}",
        cpa_usd_min=15,
        cpa_usd_max=150,
        cpa_model="recurring",
        recurring_months=12,
        notes_es="30% durante 12 meses. OJO: prohíbe ads pagados. Núcleo del nicho.",
    ),
    AffiliateProgram(
        id="elevenlabs",
        display_name="ElevenLabs (Voz IA)",
        category="ai_tool",
        landing_url="https://elevenlabs.io/",
        affiliate_url_template="https://elevenlabs.io/?from=tucanal&{utm}",
        cpa_usd_min=10,
        cpa_usd_max=120,
        cpa_model="recurring",
        recurring_months=12,
        cookie_days=90,
        notes_es="22% durante 12 meses. Coherente: tu propio canal usa ElevenLabs.",
    ),
    AffiliateProgram(
        id="lovable",
        display_name="Lovable (App builder con IA)",
        category="ai_tool",
        landing_url="https://lovable.dev/",
        affiliate_url_template="https://lovable.dev/?via=tucanal&{utm}",
        cpa_usd_min=10,
        cpa_usd_max=100,
        cpa_model="recurring",
        recurring_months=12,
        notes_es="20% durante 12 meses. Para tutoriales de crear apps/landings con IA.",
    ),
    AffiliateProgram(
        id="hostinger_vps",
        display_name="Hostinger VPS (self-hosting n8n)",
        category="hosting_vps",
        landing_url="https://www.hostinger.com/vps-hosting",
        affiliate_url_template="https://www.hostinger.com/?REFERRALCODE=tucanal&{utm}",
        cpa_usd_min=40,
        cpa_usd_max=120,
        cpa_model="per_signup",
        notes_es="40-60% pago ÚNICO (no recurrente). Para videos de n8n self-hosted en VPS.",
    ),
    AffiliateProgram(
        id="gohighlevel",
        display_name="GoHighLevel (CRM + automatización agencias)",
        category="crm_realestate",
        landing_url="https://www.gohighlevel.com/",
        affiliate_url_template="https://www.gohighlevel.com/?fp_ref=tucanal&{utm}",
        cpa_usd_min=40,
        cpa_usd_max=480,
        cpa_model="recurring",
        recurring_months=12,
        notes_es="40% recurrente. CRM usado por agencias/inmobiliarias. Ticket alto.",
    ),
]


def get_program(program_id: str) -> AffiliateProgram:
    for p in AFFILIATE_CATALOG:
        if p.id == program_id:
            return p
    raise KeyError(f"Programa de afiliado '{program_id}' no existe en el catálogo.")


def programs_for_profile(profile: NicheProfile) -> list[AffiliateProgram]:
    """Devuelve los programas referenciados en `affiliate_focus` del perfil,
    en el mismo orden. Ignora IDs no encontrados con un warning silencioso.
    """
    out: list[AffiliateProgram] = []
    for focus in profile.affiliate_focus:
        try:
            out.append(get_program(focus.id))
        except KeyError:
            continue
    return out
