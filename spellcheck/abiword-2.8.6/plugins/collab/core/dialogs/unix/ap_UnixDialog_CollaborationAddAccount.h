/* AbiCollab- Code to enable the modification of remote documents.
 * Copyright (C) 2006 by Marc Maurer <uwog@uwog.net>
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

#ifndef AP_UNIXDIALOG_COLLABORATIONADDACCOUNT_H
#define AP_UNIXDIALOG_COLLABORATIONADDACCOUNT_H

#include <gtk/gtk.h>
#include <xp/ap_Dialog_CollaborationAddAccount.h>

class XAP_Frame;

class AP_UnixDialog_CollaborationAddAccount : public AP_Dialog_CollaborationAddAccount
{
public:
	AP_UnixDialog_CollaborationAddAccount(XAP_DialogFactory * pDlgFactory, XAP_Dialog_Id id);
	static XAP_Dialog * static_constructor(XAP_DialogFactory * pFactory, XAP_Dialog_Id id);
	void						runModal(XAP_Frame * pFrame);

	void						eventOk();
	void						eventAccountTypeChanged();

protected:
	virtual void*				_getEmbeddingParent()
		{ return m_wEmbeddingParent; }
	virtual AccountHandler*		_getActiveAccountHandler();

private:
	GtkWidget*	 				_constructWindow(void);
	void						_populateWindowData(void);


	GtkWidget*					m_wWindowMain;
	GtkWidget*					m_wAccountType;
	GtkTreeModel*				m_model;
	GtkVBox*					m_wEmbeddingParent;
	GtkWidget*					m_wOk;
};

#endif /* AP_UNIXDIALOG_COLLABORATIONADDACCOUNT_H */
