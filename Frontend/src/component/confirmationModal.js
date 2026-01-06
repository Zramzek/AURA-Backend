export class ConfirmationModal {
  constructor() {
    this.injectStyles();
  }

  injectStyles() {
    if (document.getElementById("confirmation-modal-styles")) return;
    const style = document.createElement("style");
    style.id = "confirmation-modal-styles";
    style.textContent = `
      .confirmation-modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s ease, visibility 0.3s ease;
      }

      .confirmation-modal-overlay.active {
        opacity: 1;
        visibility: visible;
      }

      .confirmation-modal-box {
        background: white;
        padding: 24px;
        border-radius: 12px;
        width: 90%;
        max-width: 400px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transform: translateY(20px);
        transition: transform 0.3s ease;
        text-align: center;
      }

      .confirmation-modal-overlay.active .confirmation-modal-box {
        transform: translateY(0);
      }

      .confirmation-modal-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
      }

      .confirmation-modal-message {
        font-size: 14px;
        color: #666;
        margin-bottom: 24px;
      }

      .confirmation-modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
      }

      .confirmation-modal-btn {
        padding: 10px 20px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        border: none;
        transition: background 0.2s;
      }

      .confirmation-modal-btn.cancel {
        background: #f5f5f5;
        color: #666;
      }

      .confirmation-modal-btn.cancel:hover {
        background: #e0e0e0;
      }

      .confirmation-modal-btn.confirm {
        background: #ec1d25;
        color: white;
      }

      .confirmation-modal-btn.confirm:hover {
        background: #c91920;
      }
    `;
    document.head.appendChild(style);
  }

  show(title, message) {
    return new Promise((resolve) => {
      const modalHTML = `
        <div class="confirmation-modal-overlay active">
          <div class="confirmation-modal-box">
            <div class="confirmation-modal-title">${title}</div>
            <div class="confirmation-modal-message">${message}</div>
            <div class="confirmation-modal-actions">
              <button class="confirmation-modal-btn cancel">Batal</button>
              <button class="confirmation-modal-btn confirm">Ya, Keluar</button>
            </div>
          </div>
        </div>
      `;

      document.body.insertAdjacentHTML("beforeend", modalHTML);
      const overlay = document.body.lastElementChild;
      const cancelBtn = overlay.querySelector(".cancel");
      const confirmBtn = overlay.querySelector(".confirm");

      const cleanup = () => {
        overlay.classList.remove("active");
        setTimeout(() => overlay.remove(), 300);
      };

      cancelBtn.onclick = () => {
        cleanup();
        resolve(false);
      };

      confirmBtn.onclick = () => {
        cleanup();
        resolve(true);
      };

      // Close on outside click
      overlay.onclick = (e) => {
        if (e.target === overlay) {
          cleanup();
          resolve(false);
        }
      };
    });
  }
}

export const confirmationModal = new ConfirmationModal();