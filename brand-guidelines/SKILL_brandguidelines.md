---
name: brand-guidelines
description: Applies Kyte's official brand colors and typography to any sort of artifact that may benefit from having Kyte's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
---

# Kyte Brand Styling

## Overview

To access Kyte's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Kyte brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- Primary: `#363F4D` - Primary brand color (Dark Charcoal/Navy)
- Accent: `#2DD1AC` - Secondary accent color (Vibrant Teal)
- Background: `#FFFFFF` - Light backgrounds

**UI Colors:**

- Primary Text: `#363F4D` - Primary text color
- Link: `#2DD1AC` - Link color

**Color Application:**
- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems

### Typography

- **Headings**: Graphik (with Arial fallback)
- **Body Text**: Roboto (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

**Font Sizes:**
- H1: 52px
- H2: 36px
- Body: 16px

### Spacing & Layout

- **Base Unit**: 4px
- **Border Radius**: 4px (slightly rounded)

### UI Components

**Button Primary:**
- Background: `#2DD1AC` (Vibrant Teal)
- Text Color: `#FFFFFF` (White)
- Border Radius: 4px
- Shadow: none

**Button Secondary:**
- Background: `#FFFFFF`
- Text Color: `#363F4D`
- Border Color: `#363F4D`
- Border Radius: 4px

### Brand Personality

- **Tone**: Modern
- **Energy**: Medium
- **Target Audience**: Small business owners

### Brand Assets

- **Logo**: https://cdn.prod.website-files.com/60870ff4852ead369670e13e/60870ff4852eadba2b70e3bd_logotest.svg
- **Favicon**: https://cdn.prod.website-files.com/60870ff4852ead369670e13e/60870ff4852ead759670e169_favicon.png
- **Source URL**: https://www.kyteapp.com/kyte-for-pc

## Features

### Smart Font Application

- Applies Graphik font to headings
- Applies Roboto font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings: Graphik font, `#363F4D`
- Body text: Roboto font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors (`#2DD1AC`)
- Primary color for main brand elements
- Accent color for calls-to-action and highlights
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Graphik and Roboto fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems
