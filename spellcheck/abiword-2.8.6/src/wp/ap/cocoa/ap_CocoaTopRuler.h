/* -*- mode: C++; tab-width: 4; c-basic-offset: 4; -*- */

/* AbiWord
 * Copyright (C) 1998 AbiSource, Inc.
 * Copyright (C) 2001-2002 Hubert Figuiere
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  
 * 02111-1307, USA.
 */

#ifndef AP_COCOATOPRULER_H
#define AP_COCOATOPRULER_H

// Class for dealing with the horizontal ruler at the top of
// a document window.

/*****************************************************************/

#import <Cocoa/Cocoa.h>

#include "ut_types.h"
#include "ap_TopRuler.h"

class XAP_Frame;
@class AP_CocoaTopRulerDelegate;


/*****************************************************************/

class AP_CocoaTopRuler : public AP_TopRuler
{
public:
	AP_CocoaTopRuler(XAP_Frame * pFrame);
	virtual ~AP_CocoaTopRuler(void);

	virtual void	setView(AV_View * pView);

	// cheats for the callbacks
	void 				getWidgetPosition(int * x, int * y);
	XAP_CocoaNSView * 		getWidget(void) { return m_wTopRuler; };
	NSWindow * 	getRootWindow(void);
	
protected:
#if 0
	virtual void	_drawMarginProperties(const UT_Rect * pClipRect, AP_TopRulerInfo * pInfo, GR_Graphics::GR_Color3D clr);
	virtual void	_drawLeftIndentMarker(UT_Rect & r, bool bFilled);
	virtual void	_drawRightIndentMarker(UT_Rect & r, bool bFilled);
	virtual void	_drawFirstLineIndentMarker(UT_Rect & rect, bool bFilled);
	virtual void	_drawColumnGapMarker(UT_Rect & rect);
	virtual void	_drawCellMark(UT_Rect * prDrag, bool bUp);
#endif

private:
	static bool _graphicsUpdateCB(NSRect * aRect, GR_CocoaCairoGraphics *pG, void* param);

	XAP_CocoaNSView *			m_wTopRuler;
	NSWindow *	m_rootWindow;
	AP_CocoaTopRulerDelegate*	m_delegate;
};

#endif /* AP_COCOATOPRULER_H */
