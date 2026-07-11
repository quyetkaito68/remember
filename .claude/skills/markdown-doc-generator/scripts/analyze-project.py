#!/usr/bin/env python3
"""
Project Analyzer - Phân tích project, trích xuất metadata cho documentation
Usage: python analyze-project.py [path] [options]
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime

@dataclass
class ProjectInfo:
    name: str = ""
    description: str = ""
    version: str = ""
    language: str = ""
    framework: str = ""
    package_manager: str = ""
    license: str = ""
    author: str = ""
    repository: str = ""
    homepage: str = ""
    entry_points: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)
    dev_dependencies: Dict[str, str] = field(default_factory=dict)
    scripts: Dict[str, str] = field(default_factory=dict)
    config_files: List[str] = field(default_factory=list)
    test_files: List[str] = field(default_factory=list)
    doc_files: List[str] = field(default_factory=list)
    folder_structure: Dict[str, Any] = field(default_factory=dict)
    git_info: Dict[str, Any] = field(default_factory=dict)
    tech_stack: Dict[str, str] = field(default_factory=dict)

class ProjectAnalyzer:
    def __init__(self, root_path: Path):
        self.root = root_path.resolve()
        self.info = ProjectInfo(name=self.root.name)

    def analyze(self) -> ProjectInfo:
        """Run all analysis steps."""
        self._detect_language_and_framework()
        self._read_package_files()
        self._read_config_files()
        self._scan_entry_points()
        self._scan_tests()
        self._scan_docs()
        self._get_git_info()
        self._build_folder_structure()
        self._detect_tech_stack()
        return self.info

    def _detect_language_and_framework(self):
        """Detect primary language and framework from files."""
        # Language detection by file extensions
        ext_counts = {}
        for ext in ['.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.java', '.kt', '.cs', '.php', '.rb', '.swift']:
            count = len(list(self.root.rglob(f'*{ext}')))
            if count > 0:
                ext_counts[ext] = count

        if ext_counts:
            primary_ext = max(ext_counts, key=ext_counts.get)
            lang_map = {
                '.ts': 'TypeScript', '.tsx': 'TypeScript',
                '.js': 'JavaScript', '.jsx': 'JavaScript',
                '.py': 'Python', '.go': 'Go', '.rs': 'Rust',
                '.java': 'Java', '.kt': 'Kotlin', '.cs': 'C#',
                '.php': 'PHP', '.rb': 'Ruby', '.swift': 'Swift',
            }
            self.info.language = lang_map.get(primary_ext, 'Unknown')

        # Framework detection from package.json, Cargo.toml, etc.
        self._detect_framework_from_configs()

    def _detect_framework_from_configs(self):
        """Detect framework from config files."""
        # package.json
        pkg_json = self.root / 'package.json'
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding='utf-8'))
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                frameworks = {
                    'react': 'React', 'vue': 'Vue.js', 'svelte': 'Svelte',
                    'next': 'Next.js', 'nuxt': 'Nuxt.js', 'astro': 'Astro',
                    'express': 'Express', 'fastify': 'Fastify', 'koa': 'Koa',
                    'nest': 'NestJS', 'angular': 'Angular',
                    'electron': 'Electron', 'tauri': 'Tauri',
                    'jest': 'Jest', 'vitest': 'Vitest', 'cypress': 'Cypress',
                    'tailwindcss': 'Tailwind CSS', 'styled-components': 'Styled Components',
                    'typescript': 'TypeScript', 'webpack': 'Webpack', 'vite': 'Vite',
                }
                for key, name in frameworks.items():
                    if any(key in dep for dep in deps):
                        if not self.info.framework:
                            self.info.framework = name
                        else:
                            self.info.framework += f', {name}'
            except:
                pass

        # Cargo.toml
        cargo = self.root / 'Cargo.toml'
        if cargo.exists() and not self.info.framework:
            try:
                import tomli
                data = tomli.loads(cargo.read_text(encoding='utf-8'))
                deps = data.get('dependencies', {})
                frameworks = {
                    'actix-web': 'Actix Web', 'axum': 'Axum', 'rocket': 'Rocket',
                    'warp': 'Warp', 'tokio': 'Tokio', 'async-std': 'async-std',
                    'serde': 'Serde', 'diesel': 'Diesel', 'sqlx': 'SQLx',
                    'tauri': 'Tauri', 'egui': 'egui', 'bevy': 'Bevy',
                }
                for key, name in frameworks.items():
                    if key in deps:
                        if not self.info.framework:
                            self.info.framework = name
                        else:
                            self.info.framework += f', {name}'
            except:
                pass

        # pyproject.toml / setup.py / requirements.txt
        for py_file in ['pyproject.toml', 'setup.py', 'requirements.txt']:
            f = self.root / py_file
            if f.exists() and not self.info.framework:
                content = f.read_text(encoding='utf-8')
                frameworks = {
                    'django': 'Django', 'flask': 'Flask', 'fastapi': 'FastAPI',
                    'starlette': 'Starlette', 'tornado': 'Tornado', 'bottle': 'Bottle',
                    'pytest': 'pytest', 'celery': 'Celery', 'sqlalchemy': 'SQLAlchemy',
                    'pydantic': 'Pydantic', 'typer': 'Typer', 'click': 'Click',
                }
                for key, name in frameworks.items():
                    if key in content.lower():
                        if not self.info.framework:
                            self.info.framework = name
                        else:
                            self.info.framework += f', {name}'

        # go.mod
        go_mod = self.root / 'go.mod'
        if go_mod.exists() and not self.info.framework:
            content = go_mod.read_text(encoding='utf-8')
            frameworks = {
                'gin': 'Gin', 'echo': 'Echo', 'fiber': 'Fiber',
                'chi': 'Chi', 'gorilla/mux': 'Gorilla Mux',
                'grpc': 'gRPC', 'graphql': 'GraphQL',
            }
            for key, name in frameworks.items():
                if key in content:
                    if not self.info.framework:
                        self.info.framework = name
                    else:
                        self.info.framework += f', {name}'

    def _read_package_files(self):
        """Read package.json, Cargo.toml, pyproject.toml, etc."""
        # package.json
        pkg = self.root / 'package.json'
        if pkg.exists():
            try:
                data = json.loads(pkg.read_text(encoding='utf-8'))
                self.info.name = data.get('name', self.info.name)
                self.info.version = data.get('version', '')
                self.info.description = data.get('description', '')
                self.info.license = data.get('license', '')
                self.info.author = data.get('author', '')
                self.info.repository = data.get('repository', '')
                if isinstance(self.info.repository, dict):
                    self.info.repository = self.info.repository.get('url', '')
                self.info.homepage = data.get('homepage', '')
                self.info.scripts = data.get('scripts', {})
                self.info.dependencies = data.get('dependencies', {})
                self.info.dev_dependencies = data.get('devDependencies', {})
                self.info.package_manager = 'npm'
                # Detect pnpm/yarn
                if (self.root / 'pnpm-lock.yaml').exists():
                    self.info.package_manager = 'pnpm'
                elif (self.root / 'yarn.lock').exists():
                    self.info.package_manager = 'yarn'
                elif (self.root / 'package-lock.json').exists():
                    self.info.package_manager = 'npm'
            except:
                pass

        # Cargo.toml
        cargo = self.root / 'Cargo.toml'
        if cargo.exists():
            try:
                import tomli
                data = tomli.loads(cargo.read_text(encoding='utf-8'))
                pkg_data = data.get('package', {})
                self.info.name = pkg_data.get('name', self.info.name)
                self.info.version = pkg_data.get('version', '')
                self.info.description = pkg_data.get('description', '')
                self.info.license = pkg_data.get('license', '')
                self.info.authors = pkg_data.get('authors', [])
                self.info.repository = pkg_data.get('repository', '')
                self.info.homepage = pkg_data.get('homepage', '')
                self.info.dependencies = data.get('dependencies', {})
                self.info.package_manager = 'cargo'
            except:
                pass

        # pyproject.toml
        pyproject = self.root / 'pyproject.toml'
        if pyproject.exists():
            try:
                import tomli
                data = tomli.loads(pyproject.read_text(encoding='utf-8'))
                project = data.get('project', {})
                self.info.name = project.get('name', self.info.name)
                self.info.version = project.get('version', '')
                self.info.description = project.get('description', '')
                self.info.license = project.get('license', {}).get('text', '') if isinstance(project.get('license'), dict) else project.get('license', '')
                self.info.authors = [a.get('name', '') for a in project.get('authors', [])]
                self.info.dependencies = {dep.split('>=')[0].split('==')[0].strip(): dep for dep in project.get('dependencies', [])}
                self.info.package_manager = 'pip'
                # Check for poetry/pdm
                if 'poetry' in data.get('tool', {}):
                    self.info.package_manager = 'poetry'
                elif 'pdm' in data.get('tool', {}):
                    self.info.package_manager = 'pdm'
            except:
                pass

    def _read_config_files(self):
        """Find and list config files."""
        config_patterns = [
            '*.config.*', '*.conf.*', '*.ini', '*.toml', '*.yaml', '*.yml',
            '.env*', 'docker-compose*', 'Dockerfile*', 'Makefile*',
            'tsconfig.json', 'jsconfig.json', 'vite.config.*', 'webpack.config.*',
            'jest.config.*', 'vitest.config.*', 'playwright.config.*',
            'eslint.config.*', '.eslintrc*', 'prettier.config.*', '.prettierrc*',
            'pytest.ini', 'pyproject.toml', 'setup.cfg', 'tox.ini',
            'cargo.toml', 'go.mod', 'pom.xml', 'build.gradle*',
        ]
        for pattern in config_patterns:
            for f in self.root.rglob(pattern):
                if f.is_file():
                    rel = f.relative_to(self.root)
                    self.info.config_files.append(str(rel))

        # Deduplicate
        self.info.config_files = sorted(set(self.info.config_files))

    def _scan_entry_points(self):
        """Find entry points (main files)."""
        entry_patterns = [
            'main.*', 'index.*', 'app.*', 'server.*', 'cli.*', 'run.*',
            'src/main.*', 'src/index.*', 'src/app.*',
        ]
        for pattern in entry_patterns:
            for f in self.root.rglob(pattern):
                if f.is_file() and f.suffix in ['.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.java', '.cs']:
                    rel = f.relative_to(self.root)
                    self.info.entry_points.append(str(rel))

        self.info.entry_points = sorted(set(self.info.entry_points))[:10]  # Limit

    def _scan_tests(self):
        """Find test files."""
        test_patterns = [
            '*.test.*', '*.spec.*', '*_test.*', '*Test.*',
            'test/**/*', 'tests/**/*', '__tests__/**/*', 'spec/**/*',
        ]
        for pattern in test_patterns:
            for f in self.root.rglob(pattern):
                if f.is_file():
                    rel = f.relative_to(self.root)
                    self.info.test_files.append(str(rel))

        self.info.test_files = sorted(set(self.info.test_files))[:20]  # Limit

    def _scan_docs(self):
        """Find documentation files."""
        doc_patterns = [
            'README*', 'CHANGELOG*', 'CONTRIBUTING*', 'LICENSE*', 'CODE_OF_CONDUCT*',
            'docs/**/*.md', 'doc/**/*.md', '.github/**/*.md',
            'ARCHITECTURE*', 'DESIGN*', 'SPEC*', 'RFC*',
        ]
        for pattern in doc_patterns:
            for f in self.root.rglob(pattern):
                if f.is_file():
                    rel = f.relative_to(self.root)
                    self.info.doc_files.append(str(rel))

        self.info.doc_files = sorted(set(self.info.doc_files))

    def _get_git_info(self):
        """Get git repository info."""
        try:
            # Remote URL
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=self.root, capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                self.info.git_info['remote_url'] = result.stdout.strip()

            # Current branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.root, capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                self.info.git_info['branch'] = result.stdout.strip()

            # Last commit
            result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%h %s (%an, %ar)'],
                cwd=self.root, capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                self.info.git_info['last_commit'] = result.stdout.strip()

            # Commit count
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=self.root, capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                self.info.git_info['commit_count'] = result.stdout.strip()

            # Contributors
            result = subprocess.run(
                ['git', 'shortlog', '-sn', '--all'],
                cwd=self.root, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.info.git_info['contributors'] = result.stdout.strip().split('\n')[:10]

        except:
            pass

    def _build_folder_structure(self):
        """Build simplified folder structure."""
        def scan_dir(path: Path, max_depth: int = 3, current: int = 0) -> Dict:
            if current >= max_depth:
                return {}
            result = {}
            try:
                for entry in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                    if entry.name.startswith('.'):
                        continue
                    if entry.name in ['node_modules', '__pycache__', 'target', 'dist', 'build', '.git', 'venv', 'env']:
                        continue
                    if entry.is_dir():
                        result[entry.name + '/'] = scan_dir(entry, max_depth, current + 1)
                    else:
                        result[entry.name] = 'file'
            except:
                pass
            return result

        self.info.folder_structure = scan_dir(self.root)

    def _detect_tech_stack(self):
        """Detect technology stack."""
        stack = {}

        # Database
        db_indicators = {
            'postgresql': ['pg', 'postgres', 'postgresql'],
            'mysql': ['mysql', 'mariadb'],
            'mongodb': ['mongodb', 'mongoose'],
            'redis': ['redis', 'ioredis'],
            'sqlite': ['sqlite', 'sqlite3'],
            'dynamodb': ['dynamodb'],
            'firebase': ['firebase', 'firestore'],
        }
        all_files = ' '.join([f.read_text(encoding='utf-8', errors='ignore')[:5000] for f in self.root.rglob('*') if f.is_file() and f.suffix in ['.json', '.toml', '.yaml', '.yml', '.js', '.ts', '.py', '.go', '.rs']][:20])
        all_files_lower = all_files.lower()
        for db, keywords in db_indicators.items():
            if any(kw in all_files_lower for kw in keywords):
                stack['database'] = db
                break

        # Cloud/Deployment
        cloud_indicators = {
            'aws': ['aws', 'amazon web services', 'lambda', 'ec2', 's3', 'rds', 'ecs', 'eks'],
            'gcp': ['gcp', 'google cloud', 'cloud run', 'cloud functions', 'firestore'],
            'azure': ['azure', 'microsoft azure', 'functions', 'app service'],
            'vercel': ['vercel'],
            'netlify': ['netlify'],
            'docker': ['dockerfile', 'docker-compose', 'container'],
            'kubernetes': ['kubernetes', 'k8s', 'helm', 'kubectl'],
        }
        for cloud, keywords in cloud_indicators.items():
            if any(kw in all_files_lower for kw in keywords):
                stack['deployment'] = cloud
                break

        # CI/CD
        ci_indicators = {
            'github-actions': ['.github/workflows'],
            'gitlab-ci': ['.gitlab-ci.yml'],
            'jenkins': ['Jenkinsfile'],
            'circleci': ['.circleci'],
            'travis': ['.travis.yml'],
        }
        for ci, paths in ci_indicators.items():
            if any((self.root / p).exists() for p in paths):
                stack['ci_cd'] = ci
                break

        self.info.tech_stack = stack

    def to_dict(self) -> Dict:
        return asdict(self.info)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze project and extract metadata for documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze-project.py                    # Current directory
  python analyze-project.py /path/to/project   # Specific path
  python analyze-project.py -o project.json    # Output to JSON file
  python analyze-project.py --summary          # Print human-readable summary
        """
    )

    parser.add_argument('path', nargs='?', default='.', help='Project root directory')
    parser.add_argument('-o', '--output', help='Output JSON file')
    parser.add_argument('--summary', action='store_true', help='Print human-readable summary')
    parser.add_argument('--format', choices=['json', 'dict'], default='json', help='Output format')

    args = parser.parse_args()

    root_path = Path(args.path).resolve()
    if not root_path.exists():
        print(f"Error: Path '{root_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    analyzer = ProjectAnalyzer(root_path)
    info = analyzer.analyze()

    if args.summary:
        print_summary(info)
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(info.to_json())
        print(f"Analysis written to {args.output}")
    else:
        print(info.to_json())

def print_summary(info: ProjectInfo):
    """Print human-readable summary."""
    print(f"\n{'='*50}")
    print(f"Project Analysis: {info.name}")
    print(f"{'='*50}")
    print(f"Description: {info.description or 'N/A'}")
    print(f"Version: {info.version or 'N/A'}")
    print(f"Language: {info.language or 'N/A'}")
    print(f"Framework: {info.framework or 'N/A'}")
    print(f"Package Manager: {info.package_manager or 'N/A'}")
    print(f"License: {info.license or 'N/A'}")
    print(f"Author: {info.author or 'N/A'}")
    print(f"Repository: {info.repository or 'N/A'}")

    if info.tech_stack:
        print(f"\nTech Stack:")
        for key, value in info.tech_stack.items():
            print(f"  {key}: {value}")

    if info.entry_points:
        print(f"\nEntry Points:")
        for ep in info.entry_points[:5]:
            print(f"  - {ep}")

    if info.config_files:
        print(f"\nConfig Files ({len(info.config_files)}):")
        for cf in info.config_files[:10]:
            print(f"  - {cf}")

    if info.test_files:
        print(f"\nTest Files ({len(info.test_files)}):")
        for tf in info.test_files[:10]:
            print(f"  - {tf}")

    if info.doc_files:
        print(f"\nDocumentation Files:")
        for df in info.doc_files:
            print(f"  - {df}")

    if info.git_info:
        print(f"\nGit Info:")
        for key, value in info.git_info.items():
            if isinstance(value, list):
                print(f"  {key}: {len(value)} contributors")
            else:
                print(f"  {key}: {value}")

    print(f"\n{'='*50}")

if __name__ == '__main__':
    main()