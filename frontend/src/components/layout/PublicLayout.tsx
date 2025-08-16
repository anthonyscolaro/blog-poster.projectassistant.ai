import { Outlet, Link } from 'react-router-dom'
import { useTheme } from '@/contexts/ThemeContext'
import { Moon, Sun } from 'lucide-react'

export function PublicLayout() {
  const { theme, toggleTheme } = useTheme()

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      {/* Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-2">
                <div className="h-8 w-8 rounded bg-purple-gradient flex items-center justify-center">
                  <span className="text-white font-bold text-sm">BP</span>
                </div>
                <span className="text-xl font-bold text-gray-900 dark:text-white">
                  Blog-Poster
                </span>
              </Link>
            </div>

            <div className="flex items-center space-x-8">
              <Link
                to="/features"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Features
              </Link>
              <Link
                to="/pricing"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Pricing
              </Link>
              <Link
                to="/about"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                About
              </Link>
              <Link
                to="/contact"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Contact
              </Link>
              <button
                onClick={toggleTheme}
                className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </button>
              <Link
                to="/login"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Sign in
              </Link>
              <Link
                to="/register"
                className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <Outlet />

      {/* Footer */}
      <footer className="bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                Product
              </h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <Link to="/features" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-gray-300">
                    Features
                  </Link>
                </li>
                <li>
                  <Link to="/pricing" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-gray-300">
                    Pricing
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                Company
              </h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <Link to="/about" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-gray-300">
                    About
                  </Link>
                </li>
                <li>
                  <Link to="/contact" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-gray-300">
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                Legal
              </h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <Link to="/privacy" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-gray-300">
                    Privacy
                  </Link>
                </li>
                <li>
                  <Link to="/terms" className="text-base text-gray-500 hover:text-gray-900 dark:hover:text-gray-300">
                    Terms
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-8 border-t border-gray-200 dark:border-gray-600 pt-8">
            <p className="text-base text-gray-400 text-center">
              &copy; 2024 Blog-Poster. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}